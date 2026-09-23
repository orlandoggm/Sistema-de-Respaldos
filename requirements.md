# REQUERIMIENTOS DEL SISTEMA

- El objetivo del sistema es crear copias de seguridad cada x cantidad de tiempo
- El sistema debe crear automáticamente una copia de seguridad al iniciarlo
- La copia de seguridad se debe alojar y guardar en una carpeta con un nombre del estilo añomesdiahoraminutosegundobackup (Por ejemplo: 20260922123541backup)
- La copia se va a almacenar en un NAS, en un perfil personal, por lo que se debe pedir la ruta en cada ocasión que se haga un backup por primera vez
- Se deben copiar unicamente archivos importantes, no archivos del sistema, ejecutables, accesos directos, librerías, ni cualquier otro archivo inutil
- Para practicidad, el sistema unicamente debe funcionar con terminal del sistema, no debe tener interfaz gráfica completja.
- Los archivos importantes se refiere a documentos pdf, word, excel, powerpoint, sldprt, entre otros formatos usualmente creados por aplicaciones, diseño, administración, ingeniería y un largo etcetera en una empresa. 
- Los archivos deben de almacenarse en carpetas diferentes para cada tipo de documento, es decir, en una carpeta archivos word, en otra archivos pdf, así hasta completar todos los archivos encontrados.
- No se deben necesitar de programas o sistemas externos, debe ejecutarse sin problema aunque el sistema esté recien creado
- Para evitar explorar excesivamente carpetas, se puede enfocar unicamente en copiar archivos de las carpetas principales: Escritorio, Descargas, Documentos, Imagenes, Videos
- No se deben guardar archivos de código, es decri cualquier archivo tipo vs, py, ts, js, html, etc. etc., esto porque los archivos de código ya se guardan en github.
