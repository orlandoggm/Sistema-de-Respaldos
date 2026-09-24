# Imports
from datetime import datetime
from pathlib import Path
import shutil

# Variables globales
extensiones_incluidas = (
    # Documentos de texto y lectura
    ".txt", ".rtf", ".md", ".odt", ".tex", ".pdf", ".xps", ".epub",

    # Microsoft Word
    ".doc", ".docx", ".docm", ".dot", ".dotx", ".dotm",

    # Microsoft Excel
    ".xls", ".xlsx", ".xlsm", ".xlsb", ".xlt", ".xltx", ".xltm", ".csv",

    # Microsoft PowerPoint
    ".ppt", ".pptx", ".pptm", ".pps", ".ppsx", ".ppsm", ".pot", ".potx", ".potm",

    # Microsoft Access y otros formatos Office
    ".mdb", ".accdb", ".accde", ".accdt", ".one", ".onetoc2", ".pub",

    # LibreOffice / OpenOffice
    ".ods", ".odp", ".odg", ".odb", ".ott", ".ots", ".otp",

    # Imágenes comunes
    ".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tif", ".tiff", ".webp", ".heic",
    ".heif", ".avif", ".ico", ".jfif", ".jpe", ".dib", ".tga",

    # Imágenes RAW de cámaras
    ".raw", ".cr2", ".cr3", ".nef", ".nrw", ".arw", ".sr2", ".orf", ".rw2",
    ".raf", ".dng", ".pef", ".3fr", ".erf", ".kdc", ".mos",

    # Audio
    ".mp3", ".wav", ".flac", ".aac", ".m4a", ".ogg", ".oga", ".wma", ".aiff",
    ".aif", ".ape", ".opus", ".amr", ".mid", ".midi",

    # Video
    ".mp4", ".m4v", ".mov", ".avi", ".mkv", ".wmv", ".flv", ".webm", ".mpeg",
    ".mpg", ".m2v", ".mts", ".m2ts", ".ts", ".3gp", ".3g2", ".vob",

    # Adobe Photoshop
    ".psd", ".psb",

    # Adobe Illustrator
    ".ai", ".ait", ".eps",

    # Adobe InDesign
    ".indd", ".indt", ".idml",

    # CorelDRAW
    ".cdr", ".cdt", ".cmx",

    # Affinity / diseño gráfico
    ".afdesign", ".afphoto", ".afpub",

    # Gráficos vectoriales
    ".svg", ".svgz", ".emf", ".wmf",

    # AutoCAD
    ".dwg", ".dxf", ".dwt", ".dws",

    # SolidWorks
    ".sldprt", ".sldasm", ".slddrw", ".sldlfp", ".sldblk", ".sldtm",

    # Autodesk Inventor
    ".ipt", ".iam", ".idw", ".ipn", ".ide", ".ipj",

    # CATIA
    ".catpart", ".catproduct", ".catdrawing", ".catshape", ".cgr",

    # Siemens NX / Unigraphics
    ".prt",

    # PTC Creo / Pro Engineer
    ".asm", ".drw", ".frm", ".sec", ".neu",

    # Fusion 360
    ".f3d", ".f3z", ".f2d",

    # FreeCAD
    ".fcstd",

    # SketchUp
    ".skp", ".layout",

    # Rhino
    ".3dm",

    # Blender
    ".blend",

    # 3D Studio Max
    ".max",

    # Maya
    ".ma", ".mb",

    # Cinema 4D
    ".c4d",

    # Formatos CAD / 3D neutros
    ".step", ".stp", ".iges", ".igs", ".sat", ".sab", ".x_t", ".x_b", ".xmt_txt",
    ".jt", ".3mf", ".stl", ".obj", ".ply", ".fbx", ".dae", ".glb", ".gltf",

    # BIM / arquitectura
    ".rvt", ".rfa", ".rte", ".rft", ".ifc", ".nwd", ".nwc", ".nwf", ".pln",

    # Autodesk ReCap / nube de puntos
    ".rcp", ".rcs", ".e57", ".las", ".laz", ".pts", ".xyz",

    # Ingeniería eléctrica / electrónica
    ".sch", ".brd", ".pcb", ".kicad_sch", ".kicad_pcb", ".kicad_pro",
    ".dsn", ".gbr", ".ger", ".pho", ".drl",

    # PLC / automatización industrial
    ".ap11", ".ap12", ".ap13", ".ap14", ".ap15", ".ap16", ".ap17",
    ".zap", ".zap13", ".zap14", ".zap15", ".zap16", ".zap17", ".zap18",
    ".s7p", ".s7l", ".awl",

    # LabVIEW
    ".vi", ".vit", ".ctl", ".lvproj", ".lvlib", ".lvclass",

    # MATLAB / Simulink
    ".mat", ".slx", ".mdl", ".fig",

    # Mathcad
    ".mcd", ".mcdx", ".xmcd",

    # Ansys
    ".wbpj", ".agdb", ".mechdb", ".rst", ".rth", ".cdb",

    # Abaqus
    ".cae", ".inp", ".odb",

    # CNC / manufactura
    ".nc", ".cnc", ".tap", ".gcode", ".ngc", ".apt", ".cls",

    # Mastercam
    ".mcam", ".mcamx", ".mcx", ".mcx5", ".mcx6", ".mcx7", ".mcx8", ".mcx9",

    # CAM / manufactura en general
    ".cam", ".ncc", ".cnf",

    # Diagramas / procesos
    ".vsd", ".vsdx", ".vsdm", ".vdx", ".drawio",

    # Gestión de proyectos
    ".mpp", ".mpt", ".mpx",

    # Bases de datos empresariales locales
    ".dbf", ".fdb", ".db", ".sqlite", ".sqlite3",

    # Contabilidad / administración / intercambio de datos
    ".xml", ".json", ".csv", ".tsv", ".dif", ".slk",

    # Facturación / documentos fiscales / intercambio comercial
    ".cfdi", ".edi",

    # Compresión de archivos y entregables
    ".zip", ".7z", ".rar", ".tar", ".gz", ".tgz", ".bz2", ".xz",
)

extensiones_excluidas = (
    # Ejecutables y binarios
    ".exe",
    ".msi",
    ".msix",
    ".com",
    ".scr",
    ".bin",
    ".dll",
    ".sys",
    ".drv",
    ".ocx",
    ".cpl",

    # Accesos directos
    ".lnk",
    ".url",
    ".website",

    # Scripts
    ".bat",
    ".cmd",
    ".ps1",
    ".psm1",
    ".psd1",
    ".sh",
    ".bash",
    ".zsh",
    ".fish",
    ".vbs",
    ".vbe",
    ".wsf",
    ".wsh",
    ".hta",

    # Código fuente
    ".js",
    ".jsx",
    ".mjs",
    ".cjs",
    ".ts",
    ".tsx",
    ".py",
    ".pyw",
    ".pyc",
    ".pyo",
    ".java",
    ".class",
    ".jar",
    ".c",
    ".h",
    ".cpp",
    ".cc",
    ".cxx",
    ".hpp",
    ".cs",
    ".vb",
    ".fs",
    ".php",
    ".rb",
    ".go",
    ".rs",
    ".swift",
    ".kt",
    ".kts",
    ".dart",
    ".lua",
    ".pl",
    ".pm",
    ".r",

    # Archivos web / desarrollo
    ".html",
    ".htm",
    ".css",
    ".scss",
    ".sass",
    ".less",
    ".vue",
    ".svelte",

    # Archivos compilados / objetos
    ".o",
    ".obj",
    ".lib",
    ".a",
    ".so",
    ".dylib",
    ".pdb",
    ".ilk",
    ".exp",

    # Instaladores y paquetes
    ".appx",
    ".appxbundle",
    ".msixbundle",
    ".deb",
    ".rpm",
    ".apk",
    ".ipa",
    ".pkg",

    # Imágenes de disco / sistema
    ".iso",
    ".img",
    ".vhd",
    ".vhdx",
    ".vmdk",
    ".qcow",
    ".qcow2",

    # Archivos temporales
    ".tmp",
    ".temp",
    ".bak",
    ".old",
    ".orig",
    ".swp",
    ".swo",
    ".part",
    ".partial",
    ".crdownload",
    ".download",

    # Caché
    ".cache",
    ".dmp",
    ".dump",

    # Logs
    ".log",
    ".etl",
    ".evtx",

    # Archivos de bloqueo
    ".lock",
    ".lck",
    ".pid",

    # Archivos de configuración de desarrollo
    ".ini",
    ".cfg",
    ".conf",
    ".config",
    ".toml",
    ".yaml",
    ".yml",

    # Datos usados principalmente por aplicaciones / desarrollo
    ".json",
    ".xml",

    # Bases de datos que suelen pertenecer a aplicaciones
    ".db",
    ".db3",
    ".sqlite",
    ".sqlite3",

    # Archivos de control de versiones
    ".patch",
    ".diff",

    # Torrent / descargas
    ".torrent",

    # Metadatos y miniaturas
    ".thumb",
    ".thm",

    # Fuentes instalables
    ".fon",

    # Archivos de depuración / diagnóstico
    ".mdmp",
    ".core",
    ".trace",
)

carpetas_origen = (
    Path.home() / "Desktop",
    Path.home() / "Downloads",
    Path.home() / "Documents",
    Path.home() / "Pictures",
    Path.home() / "Videos",
)
# Funciones complementarias
def pedir_destino():
    ruta_base = input("Ingresa la ruta donde se guardará el backup: ").strip()

    ruta_base = Path(ruta_base)

    nombre_carpeta = datetime.now().strftime("%Y%m%d%H%M%S") + "backup"

    ruta_backup = ruta_base / nombre_carpeta
    ruta_backup.mkdir(parents=True, exist_ok=False)

    return ruta_backup

def copiar_archivos(carpeta_destino):
    carpeta_destino = Path(carpeta_destino)

    for carpeta_origen in carpetas_origen:
        for archivo in carpeta_origen.rglob("*"):

            if (
                archivo.is_file()
                and archivo.suffix.lower() not in extensiones_excluidas
                and archivo.suffix.lower() in extensiones_incluidas
            ):
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

# Función Main
def main():
    destino = pedir_destino()
    copiar_archivos(destino)

if  __name__ == "__main__":
    main()
