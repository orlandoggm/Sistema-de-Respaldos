# Imports
from datetime import datetime
from pathlib import Path
import shutil
import os
import sys 



# Variables globales

# Se crearon exclusiones de extensiones en lugar de copiar todo y solo mantener una pequeña parte excluida,
# ya que el objetivo de este sistema de respaldos es ser más ligero y no copiar la mayoría de archivos
# o software del sistema, ya que esto haría que el almacenamiento se llene de archivos basura.

# Extensiones permitidas dentro del respaldo, se toman en cuenta una gran cantidad de archivos,
# tanto usados como no usados, así los usuarios no se preocupan por tener que avisar y se 
# tenga que cambiar el script en caso de que empiecen a usar una extensión diferente.
# De igual forma si los usuarios notan que faltan archivos importantes, se puede hacer el cambio.
extensiones_incluidas = [
    # Texto y documentos
    ".txt", ".rtf", ".md", ".odt", ".tex", ".pdf", ".xps", ".epub",

    # Microsoft Office
    ".doc", ".docx", ".docm", ".dot", ".dotx", ".dotm",
    ".xls", ".xlsx", ".xlsm", ".xlsb", ".xlt", ".xltx", ".xltm", ".csv",
    ".ppt", ".pptx", ".pptm", ".pps", ".ppsx", ".ppsm", ".pot", ".potx", ".potm",
    ".mdb", ".accdb", ".accde", ".accdt", ".one", ".onetoc2", ".pub",
    ".vsd", ".vsdx", ".vsdm", ".vdx", ".mpp", ".mpt", ".mpx",

    # LibreOffice / OpenOffice
    ".ods", ".odp", ".odg", ".odb", ".ott", ".ots", ".otp",

    # Imágenes
    ".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tif", ".tiff", ".webp", ".heic", ".heif",
    ".avif", ".ico", ".jfif", ".jpe", ".dib", ".tga", ".raw", ".cr2", ".cr3", ".nef",
    ".nrw", ".arw", ".sr2", ".orf", ".rw2", ".raf", ".dng", ".pef", ".3fr", ".erf", ".kdc", ".mos",

    # Audio
    ".mp3", ".wav", ".flac", ".aac", ".m4a", ".ogg", ".oga", ".wma", ".aiff", ".aif",
    ".ape", ".opus", ".amr", ".mid", ".midi",

    # Video
    ".mp4", ".m4v", ".mov", ".avi", ".mkv", ".wmv", ".flv", ".webm", ".mpeg", ".mpg",
    ".m2v", ".mts", ".m2ts", ".3gp", ".3g2", ".vob",

    # Diseño gráfico
    ".psd", ".psb", ".ai", ".ait", ".eps", ".indd", ".indt", ".idml", ".cdr", ".cdt",
    ".cmx", ".afdesign", ".afphoto", ".afpub", ".svg", ".svgz", ".emf", ".wmf",

    # AutoCAD / CAD
    ".dwg", ".dxf", ".dwt", ".dws", ".step", ".stp", ".iges", ".igs", ".sat", ".sab",
    ".x_t", ".x_b", ".xmt_txt", ".jt", ".3mf", ".stl", ".obj", ".ply", ".fbx", ".dae",
    ".glb", ".gltf",

    # SolidWorks / Inventor / CATIA / Creo
    ".sldprt", ".sldasm", ".slddrw", ".sldlfp", ".sldblk", ".sldtm",
    ".ipt", ".iam", ".idw", ".ipn", ".ide", ".ipj",
    ".catpart", ".catproduct", ".catdrawing", ".catshape", ".cgr",
    ".prt", ".asm", ".drw", ".frm", ".sec", ".neu",

    # Fusion 360 / FreeCAD / SketchUp / Rhino / Blender / 3D
    ".f3d", ".f3z", ".f2d", ".fcstd", ".skp", ".layout", ".3dm", ".blend", ".max",
    ".ma", ".mb", ".c4d",

    # BIM / Arquitectura
    ".rvt", ".rfa", ".rte", ".rft", ".ifc", ".nwd", ".nwc", ".nwf", ".pln",

    # Nubes de puntos / escaneo
    ".rcp", ".rcs", ".e57", ".las", ".laz", ".pts", ".xyz", ".asc", ".pcd", ".ptx",

    # CypCut / CypNest / corte láser
    ".lxd", ".lxds", ".nrp", ".nrp2", ".nsds", ".nsd", ".nspf", ".cpe",
    ".cps", ".cps2", ".plt", ".gbx", ".bl", ".slp",

    # CNC / G-code / manufactura
    ".nc", ".cnc", ".tap", ".gcode", ".ngc", ".g", ".apt", ".cls", ".ncc", ".cam", ".cnf",

    # Mastercam
    ".mcam", ".mcamx", ".mcx", ".mcx5", ".mcx6", ".mcx7", ".mcx8", ".mcx9",

    # Ingeniería eléctrica / electrónica / PCB
    ".sch", ".brd", ".pcb", ".kicad_sch", ".kicad_pcb", ".kicad_pro", ".dsn",
    ".gbr", ".ger", ".pho", ".drl",

    # PLC / Automatización industrial
    ".ap11", ".ap12", ".ap13", ".ap14", ".ap15", ".ap16", ".ap17",
    ".zap", ".zap13", ".zap14", ".zap15", ".zap16", ".zap17", ".zap18",
    ".s7p", ".s7l", ".awl",

    # LabVIEW / MATLAB / Simulink / Mathcad
    ".vi", ".vit", ".ctl", ".lvproj", ".lvlib", ".lvclass",
    ".mat", ".slx", ".mdl", ".fig", ".mcd", ".mcdx", ".xmcd",

    # CAE / simulación
    ".wbpj", ".agdb", ".mechdb", ".rst", ".rth", ".cdb",
    ".cae", ".inp", ".odb",

    # Administración / bases de datos / intercambio
    ".dbf", ".fdb", ".db", ".sqlite", ".sqlite3", ".xml", ".json", ".tsv",
    ".dif", ".slk", ".cfdi", ".edi", ".dat",

    # GIS / mapas / ingeniería civil
    ".shp", ".shx", ".prj", ".geojson", ".kml", ".kmz", ".gpx", ".qgz", ".qgs", ".mxd", ".aprx",

    # Compresión y entregables
    ".zip", ".7z", ".rar", ".tar", ".gz", ".tgz", ".bz2", ".xz"
]

# Extensiones de archivos excluidas. Estas extensiones son totalmente inaceptables dentro del
# respaldo, ya que el usuario jamas debería interactuar con ellas y son, en su mayoría, propias
# del sistema o archivos de configuración de diferentes software.
extensiones_excluidas = (
    # Ejecutables y binarios
    ".exe", ".msi", ".msix", ".com", ".scr", ".bin", ".dll", ".sys", ".drv", ".ocx", ".cpl",

    # Accesos directos
    ".lnk", ".url", ".website",

    # Scripts
    ".bat", ".cmd", ".ps1", ".psm1", ".psd1", ".sh", ".bash", ".zsh", ".fish",
    ".vbs", ".vbe", ".wsf", ".wsh", ".hta",

    # Código fuente
    ".js", ".jsx", ".mjs", ".cjs", ".ts", ".tsx", ".py", ".pyw", ".pyc", ".pyo",
    ".java", ".class", ".jar", ".c", ".h", ".cpp", ".cc", ".cxx", ".hpp", ".cs",
    ".vb", ".fs", ".php", ".rb", ".go", ".rs", ".swift", ".kt", ".kts", ".dart",
    ".lua", ".pl", ".pm", ".r", ".md",

    # Archivos web / desarrollo
    ".html", ".htm", ".css", ".scss", ".sass", ".less", ".vue", ".svelte",

    # Archivos compilados / objetos
    ".o", ".obj", ".lib", ".a", ".so", ".dylib", ".pdb", ".ilk", ".exp",

    # Instaladores y paquetes
    ".appx", ".appxbundle", ".msixbundle", ".deb", ".rpm", ".apk", ".ipa", ".pkg",

    # Imágenes de disco / sistema
    ".iso", ".img", ".vhd", ".vhdx", ".vmdk", ".qcow", ".qcow2",

    # Archivos temporales
    ".tmp", ".temp", ".bak", ".old", ".orig", ".swp", ".swo", ".part", ".partial",
    ".crdownload", ".download",

    # Caché, logs y archivos de bloqueo
    ".cache", ".dmp", ".dump", ".log", ".etl", ".evtx", ".lock", ".lck", ".pid",

    # Configuración de desarrollo
    ".ini", ".cfg", ".conf", ".config", ".toml", ".yaml", ".yml",

    # Datos / bases de datos de aplicaciones
    ".json", ".xml", ".db", ".db3", ".sqlite", ".sqlite3",

    # Control de versiones y descargas
    ".patch", ".diff", ".torrent",

    # Metadatos, miniaturas y fuentes
    ".thumb", ".thm", ".fon",

    # Depuración / diagnóstico
    ".mdmp", ".core", ".trace",
)

carpetas_origen = (
    Path.home() / "Desktop",
    Path.home() / "Downloads",
    Path.home() / "Documents",
    Path.home() / "Pictures",
    Path.home() / "Videos",
)
# Funciones complementarias

# Esta función se encarga de pedir al usuario el destino donde se guardarán los archivos 
# la primera vez que se ejecuta. Este paso lo debe realizar el administrador encargado de 
# configurar el sistema de respaldos
import sys
from pathlib import Path
from datetime import datetime

def pedir_destino():
    if len(sys.argv) < 2:
        print("No se proporcionó la ruta donde guardar los backups.")
        return None

    carpeta_base = Path(sys.argv[1])

    nombre_backup = datetime.now().strftime("%Y%m%d%H%M%S") + "backup"

    carpeta_destino = carpeta_base / nombre_backup

    carpeta_destino.mkdir(
        parents=True,
        exist_ok=False
    )

    return carpeta_destino

# Esta función se encarga de acceder una a una a las carpetas (empezando por las carpetas_origen)
# y revisa individualmente cada archivo y su extensión para ver si copia el archvio o no. 
# La función también se encarga de recrear la misma estructura de carpetas para que el usuario
# pueda encontrar más facilmente algun archivo que quiera recuperar
def copiar_archivos(carpeta_destino):
    carpeta_destino = Path(carpeta_destino)
    contador_total = 0

    for carpeta_origen in carpetas_origen:
        print(f"copiando carpeta {carpeta_origen}")
        print(f"\nProcesando carpeta: {carpeta_origen}")
        
        if not carpeta_origen.exists():
            print(f"La carpeta no existe: {carpeta_origen}")
            continue

        try:
            for archivo in carpeta_origen.rglob("*"):

                try:
                    if (
                        archivo.is_file()
                        and archivo.suffix.lower() not in extensiones_excluidas
                        and archivo.suffix.lower() in extensiones_incluidas
                    ):
                        #print(f"Copiando archivo: {archivo}")

                        ruta_relativa = archivo.relative_to(carpeta_origen)

                        destino_archivo = (
                            carpeta_destino
                            / carpeta_origen.name
                            / ruta_relativa
                        )

                        destino_archivo.parent.mkdir(
                            parents=True,
                            exist_ok=True
                        )

                        shutil.copy2(archivo, destino_archivo)
                        contador_total += 1

                except (PermissionError, OSError) as error:
                    print(f"Error con el archivo: {archivo}")
                    print(f"Motivo: {error}")

        except (PermissionError, OSError) as error:
            print(f"No se pudo recorrer la carpeta: {carpeta_origen}")
            print(f"Motivo: {error}")

    return contador_total



# Función Main
def main():
    ruta_destino = pedir_destino()
    contador_total = copiar_archivos(ruta_destino)
    print(f"Total de archivos copiados: {contador_total}")
    input("Presione cualquier tecla para continuar...")

if  __name__ == "__main__":
    main()
