# Sistema de Respaldos 

## Descripción

Sistema que se encarga de respaldar los archivos de tu computadora en una ruta específica. Los archivos respaldados son unicamente archivos importantes, es decir aquellos archivos con los que el usuario suele trabajar, como son archivos pdf, docx, xlsx, pptx, extensiones de programas de diseño industrial, arquitectura, entre otros.

## Funcionamiento

El sistema necesita un argumento, el cual es la ruta destino. Esto se explica mejor en el apartado de Como usar. El sistema empieza a hacer la copia de seguridad desde las rutas:
- Desktop
- Downloads
- Documents
- Pictures
- Videos
No se toman en cuenta rutas padres de estas dado a que se busca minimizar la cantidad de archivos basura respaldados, el objetivo del sistema es unicamente respaldar documentos o archivos que le usuario realmente vaya a necesitar y con los que trabaje, y no se puedan recuperar o volver a descargar facilmente.
Una vez iniciado el programa empieza automaticamente a hacer esta copia de seguridad en una carpeta llamada con un formato añomesdiahoraminutossegundosbackup, (por ejemplo 20260925091256backup).
El sistema no tiene internamente un funcionamiento cíclico, si queremos que el sistema se ejecute cada cierto tiempo, se realiza mediante el programador de tareas de windows.

## Archivos respaldados

Las extensiones de archivos que se respaldan utilizando este sistema son las siguientes:
    ## Texto y documentos
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

Cualquier otra extensión se descarta automáticamente. 

## ¿Como usarlo?

El repostiorio no cuenta con el archivo ejecutable, ni el programa cuenta con un programador automático, para esto realizaremos los siguientes pasos:

1. Descargar PyInstaller
Ejecuta el siguiente comando para installar PyInstaller
```bash
pip install pyinstaller
```

2. Crear archivo .exe
Ejecuta el siguiente comando para crear el archivo .exe
```bash
python -m PyInstaller --onefile backup.py 
```
Esto creará un archivo .exe almacenado en la carpeta /dist

3. Guardar el archivo
Guarda el ejecutable en una carpeta diferente, preferentemente dentro de la raíz del disco, en su propia carpeta, por ejemplo: C:\BackupSystem\backup.exe

4. Configurar el programador de tareas
Habiendo definido la carpeta donde se encuentra el ejecutable y donde se va a almacenar el respaldo (tomaremos como ejemplo la ruta C:\BackupSystem\backup.exe como ubicación del ejecutable y \\192.168.1.10\orlando_garcia como ruta destino), hay que configurar lo siguiente en el programador de tareas

    1. Ingresar a Crear Tarea
    2. En la pestaña general, configurar nombre y descripción (no importa el contenido, pero de preferencia se específico) y asegurate que en la parte de "Al ejecutar la tarea, usar esta cuenta de usuario" se haya elegido al usuario al cual se va a hacer el respaldo. Activar "Ejecutar solo cuando el usuario haya iniciado sesión", activar "Ejecutar con los privilegios más altos" y configurar para Windows 10 (o para una versión menor en caso de que la computadora no tenga windows 10). 
    3. En la pestaña desencadenadores, crear uno nuevo con los siguientes campos: Iniciar la tarea Según la programación, la configuración depende de las necesidades del sistema, pero aquí se configura el intervalo de tiempo en el que se va a ejecutar. En configuración avanzada, unicamente es necesario activar "Detener la tarea si se ejecuta por más de", esto es a criterio del personal que configure el programa, pero por lo general es recomendable usar la opción 4 horas.
    4. En la pestaña acciones, la acción es "Iniciar un programa". En la configuración, especificamos las rutas que habíamos definido antes, tomando nuestras rutas de ejemplo quedaría: en "Programa o script" va C:\BackupSystem\backup.exe, y en "Agregar argumentos" va \\192.168.1.10\orlando_garcia, el resto de campos pueden quedar vacíos.
    5. En la pestaña condiciones, todo puede quedar desactivado.
    6. En la petaña configuración, asegurate de marcar el campo "Ejecutar la tarea lo antes posible si no hubo inicio programado".
    7. Una vez configurado todos estos campos, hacer click en aceptar y nuestra tarea estará lista para ejecutarse periodicamente.

