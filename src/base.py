# -*- coding: utf-8 -*-

import sqlite3 as lite
import sys

class BaseDeDatos:
    '''Es la clase que se encarga de la base de datos'''
    def __init__(self):
        '''Inicia self.conexion y crea las tablas si no existen'''
        # Realizamos la self.conection self.con la base de datos. De no existir, se crea.
        self.con = lite.connect('base.db')
        # El "self.cur" seria el manejador de todas las funciones SQL. 
        self.cur = self.con.cursor()
        # self.con "self.cur.execute", llamamos a la función SQL que necesitemos, en este caso, creamos la Tabla Cancion   
        self.cur.execute("CREATE TABLE IF NOT EXISTS Cancion(id int(100) not null, nombre TEXT(30) not null, artista TEXT(30) not null, album TEXT(30) not null, genero TEXT(30) not null, fecha TEXT(30) not null, pista int(100) not null, primary key(id))")
        # Creamos la tabla Lista (Si ya existe, no se crea)   
        self.cur.execute("CREATE TABLE IF NOT EXISTS Lista (id int(100) not null, cancion TEXT(100) not null, primary key(id))")
        # Creamos la tabla Perfil (Si ya existe, no se crea)
        self.cur.execute("CREATE TABLE IF NOT EXISTS Perfil (usuario TEXT not null, password TEXT not null, primary key(usuario))")
        # Creamos la tabla crea (Si ya existe, no se crea)    
        self.cur.execute("CREATE TABLE IF NOT EXISTS crea (idUsuario TEXT NOT NULL , idLista INTEGER NOT NULL )")
        # Creamos la tabla pertenece (Si ya existe, no se crea)
        self.cur.execute("CREATE TABLE IF NOT EXISTS pertenece (idCancion INTEGER NOT NULL , idLista INTEGER NOT NULL )")
        # Utilizando "self.con.commit()" establecemos los cambios
        self.con.commit()

    def nuevoPerfil(self, user, pas):
        '''Funcion para crear nuevo perfil'''
        self.cur.execute("INSERT INTO Perfil(usuario, password) VALUES(?, ?)", (user, pas))
        self.con.commit()

#    def editarPerfil(self):
        


    def close(self):
        self.con.close()

