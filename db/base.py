#!/usr/bin/python
# -*- coding: utf-8 -*-

import sqlite3 as lite
import sys

try:
#   Realizamos la coneccion con la base de datos. De no existir, se crea.    
    con = lite.connect('base.db')
    print "Conección Exitosa"
#   El "cur" seria el manejador de todas las funciones SQL. 
    cur = con.cursor()
#   Con "cur.execute", llamamos a la función SQL que necesitemos, en este caso, creamos la Tabla Cancion   
    cur.execute(
        "CREATE TABLE IF NOT EXISTS Cancion(id int(100) not null, nombre TEXT(30) not null, artista TEXT(30) not null, album TEXT(30) not null, genero TEXT(30) not null, fecha TEXT(30) not null, pista int(100) not null, primary key(id))")
    print "1"
#   Creamos la tabla Lista (Si ya existe, no se crea)   
    cur.execute(
        "CREATE TABLE IF NOT EXISTS Lista (id int(100) not null, cancion TEXT(100) not null, primary key(id))"
        )
    print "2"
#   Creamos la tabla Perfil (Si ya existe, no se crea)
    cur.execute( 
        "CREATE TABLE IF NOT EXISTS Perfil (usuario TEXT,password TEXT)"
        )
    print "3"
#   Creamos la tabla crea (Si ya existe, no se crea)    
    cur.execute(     
        "CREATE TABLE IF NOT EXISTS crea (idUsuario TEXT NOT NULL , idLista INTEGER NOT NULL )"
        )
    print "4"
#   Creamos la tabla pertenece (Si ya existe, no se crea)    
    cur.execute(     
        "CREATE TABLE IF NOT EXISTS pertenece (idCancion INTEGER NOT NULL , idLista INTEGER NOT NULL )"
        )
    print "5"
#   Utilizando "con.commit()" establecemos los cambios
    con.commit()

#Ante algun error, entra aca, ignora los cambios realizados, y muestra el error en la terminal.
except lite.Error, e:
    
    if con:
        con.rollback()
        
    print "Error %s:" % e.args[0]
    sys.exit(1)
    
finally:
#   Finalmente, despues de todo lo que se haya realizado, se cierra.    
    if con:
        con.close() 
