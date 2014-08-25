#Lucho: borra la base.db, ejecuta el base.py, el nuevoperfil.py, y ejecuta esto.

import  sqlite3 as lite
import sys
#creamos el manejador de sqlite
con = lite.connect('/home/nico/Escritorio/LNMusic/db/base.db')
cursor= con.cursor()
print "funca"

#Definimos las variables que va a utilizar el cambio de usuario. Aclaracion: las variables pasaran a ser getters cuando se lo vincule a la interfaz grafica.
user = "huguito"
pas = raw_input("cual es la contra actual?")
passNueva = raw_input("Ingrese la nueva contrasea")
print passNueva
confpas = raw_input("Confirme la nueva contrasea")
print confpas

#Definimos la funcion y le pasamos los parametros que va a requerir para cambiar la contrasena
def cambiarPass(user, pas, passNueva):
    #Si se confirma mal la contrasena no se cambia
    
    if (confpas==passNueva):
        #Actualizamos los datos de la base de datos
        code1 = "UPDATE Perfil set password=\'%s\' where usuario=\'%s\' and password=\'%s\'" % (passNueva, user, pas)
        cursor.execute(code1)
        #Guardamos los cambios para que pase algo. 
        con.commit()
    else: 
        print "pelotudo confirma bien las cosas"
        
cambiarPass(user, pas, passNueva)