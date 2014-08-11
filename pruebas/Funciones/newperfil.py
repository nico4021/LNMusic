import  sqlite3 as lite
import sys



#creamos el manejador de sqlite
con = lite.connect('/home/nico/Escritorio/LNMusic/db/base.db')
cursor= con.cursor()
print "funca"

user = "huguito"
pas = "huguitomaster1"

#Funcion para crear nuevo perfil
def nuevoPer(user, pas):
    cursor.execute("INSERT INTO Perfil(usuario, password) VALUES(?, ?)", (user, pas))
    print "paso"
    con.commit()

nuevoPer(user, pas)
