#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
METADATOS: El problema era que pedia los metadatos antes de reproducir la cancion, devolvia la lista vacia.
Se soluciona pidiendo los metadatos una vez que se reproduce el tema.
"""

from PySide import QtCore, QtGui, QtUiTools
from PySide.phonon import Phonon
import sys, pynotify, time


class Rep(QtGui.QMainWindow):
    '''Es la clase que gestiona el reproductor'''
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        
        # Cargo el archivo con los elementos graficos
        loader = QtUiTools.QUiLoader()
        self.ui = loader.load("p.ui")
        # Abro la ventana
        self.ui.show()
        
        # Creo un reproductor de tipo musica
        self.player = Phonon.createPlayer(Phonon.MusicCategory)
        
        # Conecto los eventos
        self.connect(self.ui.btnPlay, QtCore.SIGNAL("clicked()"), self.play)
        self.connect(self.ui.btnPause, QtCore.SIGNAL("clicked()"), self.pause)
        self.connect(self.player, QtCore.SIGNAL("metaDataChanged()"), self.metaData)
        
    def play(self):
        '''Reproduce un archivo'''
        # Carga el archivo de audio
        self.player.setCurrentSource(self.ui.txt.text())
        # Lo reproduce
        self.player.play()
        
    def pause(self):
        '''Pausa la reproduccion'''
        self.player.pause()
    
    def metaData(self):
        '''Devuelve los metadatos del archivo de reproduccion'''
        print self.player.metaData()


# Creo una aplicacion
app = QtGui.QApplication(sys.argv)
# Ejecuto la clase
rep = Rep()
sys.exit(app.exec_())
