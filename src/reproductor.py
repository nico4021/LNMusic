#! /usr/bin/env python
# -*- coding: utf-8 -*-

from PySide import QtCore, QtGui, QtUiTools
from PySide.phonon import Phonon
import sys, pynotify, time
from base import BaseDeDatos


class Reproductor(QtGui.QMainWindow):
    '''Es la clase que gestiona el reproductor'''
    def __init__(self, ui, login):
        QtGui.QMainWindow.__init__(self)
        
        # Creo el gestor de base de datos
        self.db = BaseDeDatos()
        
        # Cargo el archivo con los elementos graficos
        loader = QtUiTools.QUiLoader()
        self.ui = loader.load(ui)
        self.login = loader.load(login)
        # Abro la ventana
        self.ui.show()
        
        # Creo un reproductor de tipo musica
        self.player = Phonon.createPlayer(Phonon.MusicCategory)
        
        # Conecto los eventos
        self.connect(self.ui.btnPlay, QtCore.SIGNAL("clicked()"), self.play)
        self.connect(self.ui.btnAdd, QtCore.SIGNAL("clicked()"), self.abrirArchivo)
        self.connect(self.ui.actionNuevo_Perfil, QtCore.SIGNAL("triggered()"), self.nuevoPerfil)
        self.connect(self.ui.actionCerrar, QtCore.SIGNAL("triggered()"), self.ui.close)
        '''
        self.connect(self.ui.btnPause, QtCore.SIGNAL("clicked()"), self.pause)
        self.connect(self.player, QtCore.SIGNAL("metaDataChanged()"), self.metaData)
        '''
    def play(self):
        '''Reproduce un archivo'''
        # Estado del reproductor
        estado = self.player.state()
        # Si esta reproducciendo
        if estado == Phonon.State.PlayingState:
            # Pausa la reproduccion
            self.player.pause()
            # Cambia el icono
            self.ui.btnPlay.setIcon(QtGui.QIcon("img/Knob Play.png"))
        else:
            # Lo reproduce
            self.player.play()
            # Cambia el icono
            self.ui.btnPlay.setIcon(QtGui.QIcon("img/Knob Pause.png"))
        
    def pause(self):
        '''Pausa la reproduccion'''
        self.player.pause()
    
    def metaData(self):
        '''Devuelve los metadatos del archivo de reproduccion'''
        print self.player.metaData()
    
    def abrirArchivo(self):
        '''Abre un archivo de audio'''
        archivo = QtGui.QFileDialog.getOpenFileName(
            self,
            u"Abrir Archivo",
            u"/",
            u"Archivos de Audio (*.mp3 *.wav *.ogg)")
        print archivo
        
        if archivo[1]:
            self.path = archivo[0]
            self.player.setCurrentSource(self.path)

    def nuevoPerfil(self):
        '''Crea un nuevo perfil con los datos ingresados'''
        # Cambio el titulo del dialog
        self.login.setWindowTitle("Nuevo perfil")
        # Lo ejecuto
        if self.login.exec_():
            usuario = self.login.txtUsuario.text()
            contra = self.login.txtPass.text()
            # Si no se ha ingresado alguno de los campos
            if not(usuario and contra):
                # Muestro una advertencia
                QtGui.QMessageBox.warning(self, 'Advertencia!!!', u'No se han ingresado todos los campos. Por favor, elija un usuario y una contraseña para su nuevo perfil.')
            else:
                try:
                    # Creo un nuevo perfil en la base de datos
                    self.db.nuevoPerfil(usuario, contra)
                    # Muestro un mensaje de exito
                    QtGui.QMessageBox.information(self, 'Exito!!!', u'Se ha creado un nuevo perfil exitosamente.')
                # Si hay un error, (nombre de usuario repetido)
                except:
                    # Muestro una advertencia
                    QtGui.QMessageBox.warning(self, 'Advertencia!!!', 'Ya existe un perfil con ese nombre de usuario. Pruebe ingresando un usuario diferente.')
        # Limpio los campos
        self.login.txtPass.setText('')
        self.login.txtUsuario.setText('')
        
        self.login.txtUsuario.setFocus()

# Creo una aplicacion
app = QtGui.QApplication(sys.argv)
# Ejecuto la clase
rep = Reproductor("graphic.ui", "login.ui")
sys.exit(app.exec_())
