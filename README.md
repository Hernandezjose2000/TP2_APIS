Grupo 2: Game of Whiles.

Integrantes:
•	44.253.814 | Szejnfeld Sirkis, Tomas | 107710
•	42.817.690 | Palavecino Arnold, Nestor Fabian | 108244
•	95.931.033 | Hernandez Aljorna, Jose Antonio | 107411
•	42.822.519 | Espeche, Victoria | 108400


Datos acerca del TP: 
Los emails en el archivo alumnos.csv están generados ya y su contraseña para todos ellos es: amolosperros123 
El email general que se usó para el TP es: evaluaciontp2@gmail.com y su respectiva password es: Vamosaprobar . Esta password es para todos los emails excepto los que se describen a continuación, ya que son de cuentas personales:
1-	jhernandez@fi.uba.ar 
2-	antonioaljorna@gmail.com 
3-	josehernandezoboe@gmail.com 
4-	vespeche@fi.uba.ar 
5-	npalavecino@fi.uba.ar 
6-	tszejnfeld@fi.uba.ar


Pasos para la ejecución del programa:
1-	Clonar el repositorio del sistema en tu carpeta que desee: $ git clone <url_del_repositorio_remoto> 
2-	 Una vez clonado, ir a nuestro VSCode y abrir la
3-	carpeta del programa clonado y ejecutar el archivo main.py, una vez ejecutado empezara todo el sistema solicitado a crear.


ACLARACIONES:
Con el fin de facilitar al corrector el debuggueo del programa se hicieron ciertas modificaciones al archivo gmail.py. Se pasan a explicar las mismas:
1- En la función main del módulo gmail.py, específicamente la línea 272 esta comentada, debido a que cada email que lee le elimina la labelId de "UNREAD" lo cual hace que pasen a un estado de "leído" y en la query que extrae los mails, se especifica que solo traiga los emails que están marcados como "no leídos". ¿Esto que facilita al corrector? No tener que enviar un email con el formato correspondiente cada vez que quiera debuggear el programa.
2- En el módulo gmail.py, en la función obtener_ids_mails, más específicamente en la línea 131, está la query formada para extraer los mails, a esta le falta agregarle que traiga los emails de la fecha actual. ¿Esto que facilita al corrector? No estar cambiando dicha query dependiendo del día que lo ejecute el programa.


Hipótesis:
* Creamos un mail para el TP2 para que el testeo sea más fácil para todas las partes, además de que llegamos al acuerdo de que lo mejor es darle un Drive/Gmail vacío al tutor así no hay archivos personales/varios a la hora de testear las funciones de este.

* El programa crea una ruta por defecto donde se guardará TODO lo recibido por mail. La misma se crea en el Escritorio. 
RUTA_CARPETA = "EVALUACIONES"
RUTA_ENTREGAS_ALUMNOS = f"{Path.home()}/Desktop/{RUTA_CARPETA}"
En el caso que la misma ya exista no la crea, pero recibe archivos de mail de todos modos.

*Se puede elegir libremente el directorio el cual se va a ingresar desde programa.

*El usuario puede elegir libremente la ruta en donde desea guardar el archivo descargado desde Drive.

Lo mismo aplica para subir archivo al Drive, el usuario puede elegir cualquier archivo en su PC, lo único que tiene que agregar al directorio es: \nombrearchivo.extension.
Ej: C:\Users\victoria\OneDrive\Escritorio\Universidad\3er Cuatrimestre\Algoritmos y Programacion\TP_2\TP2_APIS\Programas\archivos.csv

* En cuanto el chequeo entre Gmail y carpetas, llegamos al acuerdo de chequear por padrón y no por nombre, los nombres se pueden repetir, pero el padrón es único. 

* El sistema de evaluaciones se corre para un día en particular, y en un horario que ya hayan terminado las entregas.
 
*El nombre de las carpetas de alumnos se nombran en base en al archivo alumnos.csv.

* Para que el programa pueda aceptar y descomprimir entregas, es necesario que las mismas sean en formato .zip.

* No es necesario que el zip que envíe el usuario tenga un formato en particular.

* Agregamos más opciones al menú: listar archivos en drive y mover archivos en drive, las mismas se veían mencionadas en el flujo de la funcionalidad de Drive, sin embargo, no tenían lugar en el menú. Vimos oportuno su adición para complementar las funciones de subida y descarga de archivos.

* En la opción 1, cuando se listan los archivos en local, si bien el usuario puede ver los archivos y carpetas de ese directorio en particular, también puede acceder a cualquier otro que desee usando la función de "volver atrás" (subir de nivel); y luego, por supuesto, volver a la actual, eligiendo la opción de "Ingresar a una carpeta”.
