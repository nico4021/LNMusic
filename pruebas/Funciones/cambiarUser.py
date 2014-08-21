import  sqlite3 as lite
import sys
#creamos el manejador de sqlite
con = lite.connect('/home/nico/Escritorio/LNMusic/db/base.db')
cursor= con.cursor()
print "funca"

#Definimos las variables que va a utilizar el cambio de usuario. Aclaracion: las variables pasaran a ser getters cuando se lo vincule a la interfaz grafica.
user = "huguito"
pas = "huguitomaster1"
nombreNuevo = "pez"

#Definimos la funcion y le pasamos los parametros que va a requerir para cambiar el nombre del usuario
def cambiarUser(user, pas, nombreNuevo):
    #Con "code1" borramos el perfil viejo
    code1 = "UPDATE Perfil set usuario=\'%s\' where usuario=\'%s\' and password=\'%s\'" % (nombreNuevo, user, pas)
    cursor.execute(code1)
    #Guardamos los cambios para que pase algo. 
    con.commit()
        
cambiarUser(user, pas, nombreNuevo)