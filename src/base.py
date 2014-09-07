# -*- coding: utf-8 -*-

import sqlite3 as lite
import sys

class BaseDeDatos:
    '''Es la clase que se encarga de la base de datos'''
    def __init__(self, ruta):
        '''Inicia self.conexion y crea las tablas si no existen'''
        # Realizamos la self.conection self.con la base de datos. De no existir, se crea.
        self.con = lite.connect(ruta)
        # El "self.cur" seria el manejador de todas las funciones SQL.
        self.cur = self.con.cursor()
        # self.con "self.cur.execute", llamamos a la función SQL que necesitemos, en este caso, creamos la Tabla Cancion   
        self.cur.execute("""CREATE TABLE IF NOT EXISTS Cancion(
            id integer not null primary key, 
            idLista integer not null, 
            nombre TEXT not null )""")
#            artista TEXT not null, 
#            album TEXT not null, 
#            genero TEXT not null, 
#            fecha TEXT not null, 
#            pista integer not null )""")
        # Creamos la tabla Lista (Si ya existe, no se crea)   
        self.cur.execute("""CREATE TABLE IF NOT EXISTS Lista (
            id integer not null primary key, 
            nomPerfil text not null, 
            nombre TEXT not null )""")
        # Creamos la tabla Perfil (Si ya existe, no se crea)
        self.cur.execute("""CREATE TABLE IF NOT EXISTS Perfil (
            usuario TEXT not null primary key, 
            password TEXT not null )""")
        # Utilizando "self.con.commit()" establecemos los cambios
        self.con.commit()

    def nuevoPerfil(self, user, pas):
        '''Funcion para crear nuevo perfil'''
        self.cur.execute("INSERT INTO Perfil(usuario, password) VALUES(?, ?)", (user, pas))
        self.cur.execute("INSERT INTO Lista(nomPerfil, nombre) VALUES(?, ?)", (user, u'Mi música'))
        self.con.commit()

    def editarPerfil(self, newN, newP, user, pas):
        #Guardamos los cambios para que pase algo. 
        if (confpas==passNueva):
            code = "UPDATE Perfil set usuario=\'%s\' where usuario=\'%s\' and password=\'%s\'" % (newN, user, pas)
            cursor.execute(code)
            con.commit()
            
            #Actualizamos los datos de la base de datos
            code1 = "UPDATE Perfil set password=\'%s\' where usuario=\'%s\' and password=\'%s\'" % (newP, user, pas)
            cursor.execute(code1)
            #Guardamos los cambios para que pase algo. 
            con.commit()
        else: 
            print "pelotudo confirma bien las cosas"

    def obtenerPerfil(self, user):
        '''Devuelve el perfil del usuario seleccionado o un vector vacio'''
        # Se fija si hay algun perfil con ese nombre
        self.cur.execute("SELECT * FROM Perfil WHERE usuario = \'%s\'" % user)
        return self.cur.fetchall()
    
    def obtenerUsuarios(self):
        '''Devuelve una lista de usuarios registrados'''
        # Busca todos los usuarios
        self.cur.execute("SELECT usuario FROM Perfil")
        users_db = self.cur.fetchall()
        users = []
        for i in users_db:
            users.append(i[0])
        return users
    
    def borrarPerfil(self, user):
        '''Borra el perfil seleccionado'''
        # Borra el perfil
        self.cur.execute("DELETE FROM Perfil WHERE usuario = \'%s\'" % user )
        self.con.commit()

    def nuevaLista(self, lista, perfil):
        '''Funcion para crear una nueva lista de reproduccion'''
        self.cur.execute("INSERT INTO Lista(nomPerfil, nombre) VALUES(?, ?)", (perfil, lista))
        self.con.commit()

    def obtenerIdLista(self, usuario, lista):
        '''Devuelve el id de una lista de reproduccion'''
        self.cur.execute("SELECT id FROM Lista WHERE nomPerfil = \'%s\' AND nombre = \'%s\'" % (usuario, lista))
        return self.cur.fetchall()[0][0]

    def obtenerListas(self, usuario):
        '''Devuelve una lista de listas de reproduccion de un perfil'''
        # Busca todas las listas de ese usuario
        self.cur.execute("SELECT nombre FROM Lista WHERE nomPerfil = \'%s\'" % usuario)
        listas_db = self.cur.fetchall()
        listas = []
        for i in listas_db:
            listas.append(i[0])
        return listas

    def borrarLista(self, lista, usuario):
        idLista = self.obtenerIdLista(usuario, lista)
        self.cur.execute("DELETE FROM Lista WHERE id = \'%s\'" % idLista )
        self.cur.execute("DELETE FROM Cancion WHERE idLista = \'%s\'" % idLista )
        self.con.commit()

    def agregarCanciones(self, canciones, lista, usuario):
        idLista = self.obtenerIdLista(usuario, lista)

        self.cur.execute("DELETE FROM Cancion WHERE idLista = \'%s\'" % idLista )

        for cancion in canciones:
            self.cur.execute("INSERT INTO Cancion(idLista, nombre) VALUES(%s, \'%s\')" % (idLista, cancion.text()))
        self.con.commit()

    def obtenerCanciones(self, lista, usuario):
        '''Devuelve una lista de canciones de una lista de reproduccion y un usuario'''
        idLista = self.obtenerIdLista(usuario, lista)
        # Busca todas las canciones de esa lista
        self.cur.execute("SELECT nombre FROM Cancion WHERE idLista = %s" % idLista)
        canciones_db = self.cur.fetchall()
        canciones = []
        for i in canciones_db:
            canciones.append(i[0])
        return canciones

    def close(self):
        self.cur.close()
        self.con.close()

