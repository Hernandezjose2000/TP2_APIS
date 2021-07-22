Datos acerca del TP:
-Los emails en el archivo alumnos.csv estan generados ya y su password para todos ellos es: amolosperros123
-El email general que se uso para el tp es: evaluaciontp2@gmail.com y su respectiva password es: Vamosaprobar

Esta password es para todos los emails excepto los que se describen a continuacion ya que son de cuentas personales:

1-jhernandez@fi.uba.ar
2-antonioaljorna@gmail.com
3-josehernandezoboe@gmail.com
4-vespeche@fi.uba.ar
5-npalavecino@fi.uba.ar
6-tszejnfeld@fi.uba.ar

Pasos para la ejecucion del programa:

1- Clonar el repositorio del sistema en tu carpeta que desee: git clone <url_del_repositorio_remoto>
2- Una vez clonado, ir a nuestro vscode y abrir la carpeta del programa clonado y ejecutar el archivo main.py, una vez ejecutado empezara todo el sistema solicitado a crear.


ACLARACIONES:

Con el fin de facilitar al corrector el debuggueo del programa se hicieron ciertas modificaciones al archivo gmail.py. Se pasan a explicar las mismas:

1- En la funcion main del modulo gmail.py, espcificamente la linea 272 esta comentada, debido a que cada email que lee le elimina la labelId de"UNREAD" lo cual hace que 
pasen a un estado de "leido" y en la query que extrae los mails, se especifica que solo traiga los emails que estan marcados como "no leidos". Esto que facilita al corrector? No tener que
enviar un email con el formato correspondiente cada vez que quiera debuggear el programa.

2- En el modulo gmail.py, en la funcion obtener_ids_mails, mas especificamente en la linea 131, esta la query formada para extraer los mails, a esta le falta agregarle que traiga los emails
de la fecha actual. Esto que facilita al corrector? No estar cambiando dicha query dependiendo del dia que lo ejecute el programa.

Todas estas razones se explicaran su por que en la defensa del mismo basandonos en la hipotesis establecidas para estas ocurrencias.
