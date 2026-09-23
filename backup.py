#!/usr/bin/env python3
"""
Copias de seguridad hacia un NAS (solo Windows, solo terminal, solo librería estándar).

- Solo explora las carpetas más usadas: Escritorio, Descargas, Documentos,
  Imágenes y Vídeos (las detecta aunque estén redirigidas a OneDrive o
  tengan otro nombre según el idioma de Windows).
- Hace un backup al iniciar y luego cada X minutos.
- Cada backup vive en una carpeta AAAAMMDDHHMMSSbackup (ej. 20260922123541backup).
- Cada documento se guarda en su propia subcarpeta.
- Los tipos de archivo se detectan solos (tipos registrados en Windows + firmas
  binarias + menú numerado para los dudosos). La elección se guarda en
  backup_config.json.

Uso:
    python backup_nas.py                    # pregunta lo necesario
    python backup_nas.py --intervalo 60     # backup cada 60 minutos
    python backup_nas.py --reconfigurar     # vuelve a elegir carpetas/tipos
"""

import argparse
import csv
import ctypes
import json
import mimetypes
import os
import re
import shutil
import time
import uuid
from datetime import datetime, timedelta
from pathlib import Path

CONFIG_FILE = Path(__file__).resolve().with_name("backup_config.json")

# Firmas binarias de lo que NO es un documento
FIRMAS_NO_DOCUMENTO = (
    b"MZ",                             # .exe, .dll, .sys, .scr, .ocx...
    b"L\x00\x00\x00\x01\x14\x02\x00",  # acceso directo .lnk
    b"[InternetShortcut]",             # acceso directo .url
)

# Palabras clave del tipo MIME que delatan ejecutables/instaladores
MIME_RECHAZO = ("executable", "msdownload", "dosexec", "x-msi", "installer", "x-bat")
# Tipos MIME que corresponden a código fuente, scripts o archivos de configuración
MIME_CODIGO = ("javascript", "typescript", "x-python", "x-java", "x-csrc", "x-chdr",
               "x-c++", "x-sh", "x-csh", "x-perl", "x-ruby", "x-php", "x-sql",
               "x-yaml", "json", "xml", "html", "css")

UMBRAL_CODIGO = 0.30  # % de líneas de código para considerar que un archivo es código

# Carpetas de dependencias o papelera
DIRS_RUIDO = {"node_modules", "site-packages", "__pycache__", "$recycle.bin",
              "system volume information"}

NOMBRES_RESERVADOS = {"con", "prn", "aux", "nul", *(f"com{i}" for i in range(1, 10)),
                      *(f"lpt{i}" for i in range(1, 10))}

ATTR_OCULTO_SISTEMA = 0x2 | 0x4          # oculto | sistema
ATTR_REPARSE = 0x400                     # enlaces y junctions (solo se evitan en carpetas)
ATTR_SOLO_NUBE = 0x1000 | 0x40000 | 0x400000  # archivos de OneDrive aún no descargados

# Carpetas de usuario: (nombre, GUID de carpeta conocida de Windows, nombre por defecto)
CARPETAS_USUARIO = (
    ("Escritorio", "B4BFCC3A-DB2C-424C-B029-7FE99A87C641", "Desktop"),
    ("Descargas", "374DE290-123F-4565-9164-39C4925E467B", "Downloads"),
    ("Documentos", "FDD39AD0-238F-46AF-ADB4-6C85480369C7", "Documents"),
    ("Imágenes", "33E28130-4E1E-4676-835A-98395C3BC3BB", "Pictures"),
    ("Vídeos", "18989B1D-99B5-455B-841C-AB7C74E4DDFC", "Videos"),
)

mimetypes.init()  # Windows aporta los tipos registrados por Office, SolidWorks, etc.


# ----------------------------------------------------------------------------
# Detección de "archivo importante"
# ----------------------------------------------------------------------------

def _omitir(ruta, nombre, es_carpeta):
    """Oculto, de sistema, temporal de Office (~$), o punto inicial. Además:
    carpetas que son enlaces/junctions, y archivos de OneDrive sin descargar
    (para no disparar su descarga masiva)."""
    if nombre.startswith((".", "~$")) or nombre.endswith("~"):
        return True
    try:
        attrs = getattr(os.stat(ruta, follow_symlinks=False), "st_file_attributes", 0)
    except OSError:
        return True
    bloqueo = ATTR_OCULTO_SISTEMA | (ATTR_REPARSE if es_carpeta else ATTR_SOLO_NUBE)
    return bool(attrs & bloqueo)


def _carpeta_conocida(guid):
    """Ruta real de una carpeta de usuario según Windows (respeta OneDrive e idioma)."""
    class GUID(ctypes.Structure):
        _fields_ = [("d1", ctypes.c_uint32), ("d2", ctypes.c_uint16),
                    ("d3", ctypes.c_uint16), ("d4", ctypes.c_ubyte * 8)]
    try:
        g = GUID.from_buffer_copy(uuid.UUID(guid).bytes_le)
        ruta = ctypes.c_wchar_p()
        if ctypes.windll.shell32.SHGetKnownFolderPath(ctypes.byref(g), 0, None, ctypes.byref(ruta)) == 0:
            valor = ruta.value
            ctypes.windll.ole32.CoTaskMemFree(ruta)
            return valor
    except (AttributeError, OSError):
        pass
    return None


def carpetas_usuario():
    """Devuelve [(nombre, ruta)] de las 5 carpetas más usadas que existan."""
    encontradas = []
    for nombre, guid, defecto in CARPETAS_USUARIO:
        ruta = _carpeta_conocida(guid) or str(Path.home() / defecto)
        if os.path.isdir(ruta):
            encontradas.append((nombre, os.path.abspath(ruta)))
    return encontradas


def _dirs_sistema():
    """Carpetas de sistema tomadas del entorno de Windows."""
    variables = ("WINDIR", "SYSTEMROOT", "PROGRAMFILES", "PROGRAMFILES(X86)",
                 "PROGRAMW6432", "PROGRAMDATA")
    return {os.path.normcase(os.path.abspath(os.environ[v])) for v in variables if os.environ.get(v)}


def es_ejecutable(ruta):
    """True si por su CONTENIDO es ejecutable, librería o acceso directo."""
    try:
        with open(ruta, "rb") as f:
            return f.read(32).startswith(FIRMAS_NO_DOCUMENTO)
    except OSError:
        return False

def clasificar_extension(ext, info):
    """Devuelve 'aceptar', 'revisar', 'codigo' o 'rechazar' para una extensión."""
    if info["revisados"] and info["ejecutables"] * 2 >= info["revisados"]:
        return "rechazar"
    mime, _ = mimetypes.guess_type("archivo" + ext)
    if mime and (mime.startswith("text/x-") or any(k in mime for k in MIME_CODIGO)):
        return "codigo"
    if info["revisados"] and info["codigo"] * 2 >= info["revisados"]:
        return "codigo"
    if mime is None:
        return "revisar"  # ej. .sldprt sin SolidWorks instalado
    if any(k in mime for k in MIME_RECHAZO):
        return "rechazar"
    if mime.startswith(("audio/", "video/")):
        return "revisar"
    if mime.startswith("text/"):
        return "aceptar" if mime == "text/csv" else "revisar"
    if mime.startswith(("application/", "image/")):
        return "aceptar"
    return "revisar"


# ----------------------------------------------------------------------------
# Recorrido de archivos
# ----------------------------------------------------------------------------

def recorrer(origenes, excluidos):
    """Genera rutas de archivos candidatos saltando carpetas de sistema u ocultas."""
    for origen in origenes:
        for raiz, dirs, archivos in os.walk(origen):
            dirs[:] = [
                d for d in dirs
                if d.lower() not in DIRS_RUIDO
                and not _omitir(os.path.join(raiz, d), d, True)
                and os.path.normcase(os.path.abspath(os.path.join(raiz, d))) not in excluidos
            ]
            for a in archivos:
                ruta = os.path.join(raiz, a)
                if not _omitir(ruta, a, False):
                    yield Path(ruta)


def escanear_extensiones(origenes, excluidos):
    """Cuenta extensiones y detecta cuáles son en realidad ejecutables."""
    stats, total = {}, 0
    for f in recorrer(origenes, excluidos):
        ext = f.suffix.lower()
        try:
            tam = f.stat().st_size
        except OSError:
            continue
        if not ext or tam == 0:
            continue
        e = stats.setdefault(ext, {"n": 0, "bytes": 0, "revisados": 0, "ejecutables": 0, "codigo": 0})
        e["n"] += 1
        e["bytes"] += tam
        if e["revisados"] < 5:  # solo se muestrean unos pocos archivos por extensión
            e["revisados"] += 1
            e["ejecutables"] += es_ejecutable(f)
        total += 1
        if total % 2000 == 0:
            print(f"\r  Analizando... {total} archivos", end="", flush=True)
    print(f"\r  Análisis terminado: {total} archivos con extensión.      ")
    return stats


# ----------------------------------------------------------------------------
# Configuración interactiva
# ----------------------------------------------------------------------------

def formato_tam(n):
    for unidad in ("B", "KB", "MB", "GB", "TB"):
        if n < 1024 or unidad == "TB":
            return f"{n:.0f} {unidad}" if unidad == "B" else f"{n:.1f} {unidad}"
        n /= 1024


def parsear_numeros(texto, maximo):
    res = set()
    for tok in texto.replace(",", " ").split():
        if "-" in tok:
            a, _, b = tok.partition("-")
            if a.isdigit() and b.isdigit():
                res.update(range(int(a), int(b) + 1))
        elif tok.isdigit():
            res.add(int(tok))
    return {n for n in res if 1 <= n <= maximo}


def pedir_origenes():
    """Usa las carpetas más usadas del usuario; permite indicar otras si se prefiere."""
    conocidas = carpetas_usuario()
    if conocidas:
        print("Carpetas que se respaldarán:")
        for nombre, ruta in conocidas:
            print(f"  - {nombre}: {ruta}")
    while True:
        if conocidas:
            r = input("Enter para usarlas, o escribe otras rutas separadas por ';': ").strip()
        else:
            r = input("No se encontraron carpetas de usuario. Escribe las rutas separadas por ';': ").strip()
        if not r and conocidas:
            return [ruta for _, ruta in conocidas]
        rutas = [x.strip().strip('"') for x in r.split(";") if x.strip()]
        invalidas = [x for x in rutas if not os.path.isdir(x)]
        if invalidas or not rutas:
            print("  Rutas no válidas:", ", ".join(invalidas) or "(vacío)")
            continue
        return [os.path.abspath(x) for x in rutas]


def configurar():
    print("\n=== Configuración inicial ===")
    origenes = pedir_origenes()
    print("\nBuscando tipos de archivo en tus carpetas (puede tardar)...")
    stats = escanear_extensiones(origenes, _dirs_sistema())

    aceptadas, revisar, codigo, rechazadas = [], [], [], 0
    for ext, info in stats.items():
        veredicto = clasificar_extension(ext, info)
        if veredicto == "aceptar":
            aceptadas.append(ext)
        elif veredicto == "revisar":
            revisar.append(ext)
        elif veredicto == "codigo":
            codigo.append(ext)
        else:
            rechazadas += 1

    aceptadas.sort(key=lambda e: -stats[e]["n"])
    revisar = sorted(revisar, key=lambda e: -stats[e]["n"])[:60]  # las 60 más frecuentes
    lista = aceptadas + revisar
    elegidas = set(aceptadas)

    print(f"\n{rechazadas} tipos descartados automáticamente (ejecutables, librerías, accesos directos).")
    if codigo:
        codigo.sort(key=lambda e: -stats[e]["n"])
        vista = ", ".join(codigo[:20]) + (" ..." if len(codigo) > 20 else "")
        print(f"{len(codigo)} tipos de código descartados (se asume respaldo en GitHub): {vista}")
    while True:
        print("\n  Nº  Sel  Extensión   Archivos   Tamaño       Decisión")
        for i, ext in enumerate(lista, 1):
            marca = "[x]" if ext in elegidas else "[ ]"
            origen = "reconocido por Windows" if ext in aceptadas else "dudoso / desconocido"
            print(f"  {i:>2}  {marca}  {ext:<10} {stats[ext]['n']:>8}   "
                  f"{formato_tam(stats[ext]['bytes']):>10}   {origen}")
        r = input("\nNúmeros a marcar/desmarcar (ej. 3 5-8), 'todo', 'nada' o Enter para confirmar: ").strip().lower()
        if not r:
            break
        if r == "todo":
            elegidas = set(lista)
        elif r == "nada":
            elegidas = set()
        else:
            for n in parsear_numeros(r, len(lista)):
                elegidas ^= {lista[n - 1]}

    cfg = {"origenes": origenes, "extensiones": sorted(elegidas)}
    CONFIG_FILE.write_text(json.dumps(cfg, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\nConfiguración guardada en {CONFIG_FILE.name} ({len(elegidas)} tipos de archivo).")
    return cfg


def cargar_config(reconfigurar):
    if not reconfigurar and CONFIG_FILE.exists():
        try:
            cfg = json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
            if cfg.get("origenes") and cfg.get("extensiones"):
                return cfg
        except (OSError, ValueError):
            pass
    return configurar()


# ----------------------------------------------------------------------------
# Backup
# ----------------------------------------------------------------------------

def pedir_destino():
    """Pide la ruta del NAS (ej. \\\\NAS\\usuarios\\juan o Z:\\juan) y comprueba escritura."""
    while True:
        r = input("\nRuta del NAS (perfil personal) donde guardar los backups: ").strip().strip('"')
        if not r:
            continue
        destino = Path(r)
        if not destino.is_dir():
            print("  Esa ruta no existe o no es accesible. Inténtalo de nuevo.")
            continue
        prueba = destino / "prueba_escritura.tmp"
        try:
            prueba.write_text("ok")
            prueba.unlink()
        except OSError as e:
            print(f"  No se puede escribir en esa ruta: {e}")
            continue
        return destino


def limpiar_nombre(nombre):
    nombre = re.sub(r'[<>:"/\\|?*\x00-\x1f]', "_", nombre).strip(" .")
    if nombre.split(".")[0].lower() in NOMBRES_RESERVADOS:
        nombre = "_" + nombre
    return nombre or "archivo"


def carpeta_unica(archivo, usadas):
    """Una carpeta por documento: nombre_ext, y _2, _3... si hay repetidos."""
    base = limpiar_nombre(f"{archivo.stem}_{archivo.suffix.lstrip('.')}")
    nombre, n = base, 2
    while nombre.lower() in usadas:
        nombre = f"{base}_{n}"
        n += 1
    usadas.add(nombre.lower())
    return nombre


def hacer_backup(destino_raiz, cfg):
    carpeta = Path(destino_raiz) / (datetime.now().strftime("%Y%m%d%H%M%S") + "backup")
    carpeta.mkdir(parents=True)
    print(f"\n[{datetime.now():%H:%M:%S}] Iniciando backup en {carpeta}")

    excluidos = _dirs_sistema() | {os.path.normcase(os.path.abspath(destino_raiz))}
    extensiones = set(cfg["extensiones"])
    usadas, filas, errores, total_bytes = set(), [], [], 0

    for archivo in recorrer(cfg["origenes"], excluidos):
        if archivo.suffix.lower() not in extensiones:
            continue
        try:
            if archivo.stat().st_size == 0 or es_ejecutable(archivo):
                continue
            sub = carpeta / carpeta_unica(archivo, usadas)
            sub.mkdir()
            copia = sub / limpiar_nombre(archivo.name)
            shutil.copy2(archivo, copia)
            total_bytes += copia.stat().st_size
            filas.append((str(archivo), str(copia.relative_to(carpeta))))
            if len(filas) % 50 == 0:
                print(f"\r  {len(filas)} archivos copiados...", end="", flush=True)
        except OSError as e:
            errores.append((str(archivo), str(e)))

    # Manifiesto: ruta original de cada copia (utf-8-sig para que Excel lo abra bien)
    with open(carpeta / "manifiesto.csv", "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(["ruta_original", "ruta_en_backup"])
        w.writerows(filas)
    if errores:
        with open(carpeta / "errores.csv", "w", newline="", encoding="utf-8-sig") as f:
            w = csv.writer(f)
            w.writerow(["archivo", "error"])
            w.writerows(errores)

    print(f"\r[{datetime.now():%H:%M:%S}] Backup terminado: {len(filas)} archivos "
          f"({formato_tam(total_bytes)}), {len(errores)} errores.")


def main():
    parser = argparse.ArgumentParser(description="Backups automáticos hacia un NAS.")
    parser.add_argument("--intervalo", type=float, help="minutos entre backups")
    parser.add_argument("--reconfigurar", action="store_true",
                        help="vuelve a elegir carpetas y tipos de archivo")
    args = parser.parse_args()

    cfg = cargar_config(args.reconfigurar)

    intervalo = args.intervalo
    while not intervalo or intervalo <= 0:
        try:
            intervalo = float(input("Cada cuántos minutos se hará un backup: ").replace(",", "."))
        except ValueError:
            intervalo = None

    destino = None
    print("\nSistema activo. Pulsa Ctrl+C para detenerlo.")
    try:
        while True:
            if destino is None:
                destino = pedir_destino()  # solo en el primer backup de esta ejecución
            if destino.is_dir():
                try:
                    hacer_backup(destino, cfg)
                except OSError as e:
                    print(f"\n  Error durante el backup: {e}")
            else:
                print(f"\n[{datetime.now():%H:%M:%S}] El NAS no está accesible; se reintentará en el próximo ciclo.")
            print(f"Próximo backup a las {datetime.now() + timedelta(minutes=intervalo):%H:%M:%S}")
            time.sleep(intervalo * 60)
    except KeyboardInterrupt:
        print("\nDetenido por el usuario.")


if __name__ == "__main__":
    main()