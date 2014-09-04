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
        
        # Inicio pynotify
        pynotify.init("LNMusic")
        self.noti = pynotify.Notification(' ', ' ')
        
        # Creo el gestor de base de datos
        self.db = BaseDeDatos('db/base.db')
        
        # Cargo el archivo con los elementos graficos
        loader = QtUiTools.QUiLoader()
        self.login = loader.load(login)
        self.ui = loader.load(ui)

        # Abro el login
        self.login.show()
        self.login.txtUsuario.setFocus()

        # Si se elije aceptar
        def ingresar():
            # Obtengo usuario y contraseña ingresados
            usuario = self.login.txtUsuario.text()
            contra = self.login.txtPass.text()
            # Busco en la base de datos al perfil con dicho nombre de usuario
            perfil = self.db.obtenerPerfil(usuario)

            # Si no se ha ingresado alguno de los campos
            if not(usuario and contra):
                # Muestro una advertencia
                QtGui.QMessageBox.warning(self, 'Advertencia!!!', u'No se han ingresado todos los campos. Por favor, elija un usuario y una contraseña validos.')

            # Si no existe ningun perfil con ese nombre
            elif not perfil:
                # Muestro un error
                QtGui.QMessageBox.critical(self, 'Error!!!', u'El usuario %s no existe.' % usuario)

            # Si la contraseña es incorrecta
            elif contra != perfil[0][1]:
                # Muestro un error
                QtGui.QMessageBox.critical(self, 'Error!!!', u'Contraseña incorrecta.')

            else:
                # Inicia el reproductor de musica
                self.iniciar_reproductor(usuario)

        # Conecto el evento cuando se pulsa aceptar
        self.login.btnBox.accepted.connect(ingresar)

    def iniciar_reproductor(self, titulo):
        # Abro la ventana
        self.ui.show()
        self.ui.setWindowTitle(titulo)
        
        # Creo un reproductor de tipo musica
        self.player = Phonon.createPlayer(Phonon.MusicCategory)
        self.player.setTickInterval(1000)
        
        # Creo slider del audio
        slider = Phonon.SeekSlider(self)
        slider.setMediaObject(self.player)
        
        self.ui.seekLayout.addWidget(slider)
        
        # Conecto los eventos
        self.connect(self.ui.btnPlay, QtCore.SIGNAL("clicked()"), self.play)
        self.connect(self.ui.btnAdd, QtCore.SIGNAL("clicked()"), self.abrirArchivo)
        self.connect(self.ui.actionNuevo_Perfil, QtCore.SIGNAL("triggered()"), self.nuevoPerfil)
        self.connect(self.ui.actionCerrar, QtCore.SIGNAL("triggered()"), self.ui.close)
        self.player.metaDataChanged.connect(self.metaData)
        self.player.stateChanged.connect(self.state)
        self.player.tick.connect(self.tick)
        #self.connect(self.player, QtCore.SIGNAL("metaDataChanged()"), self.metaData)

    def tick(self, time):
        '''Se encarga de llevar la cuenta del tiempo transcurrido'''
        displayTime = QtCore.QTime(0, (time / 60000) % 60, (time / 1000) % 60)
        self.ui.musicTime.setText(displayTime.toString('mm:ss'))

    def state(self, estado):
        if estado == Phonon.State.PlayingState:
            self.noti.show()

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
            print self.player.currentTime()

    def metaData(self):
        '''Devuelve los metadatos del archivo de reproduccion'''
        # Obtengo metadatos
        try:
            nombre = self.player.metaData("TITLE")[0]
        except:
            nombre = " - Sin nombre - "
        try:
            artista = self.player.metaData("ARTIST")[0]
        except:
            artista = " - Sin artista - "
        try:
            album = self.player.metaData("ALBUM")[0]
        except:
            album = " - Sin album - "
        
        # Muestro los datos 
#        print self.player.metaData()

        # Actualizo notificacion
        self.noti.update(nombre, artista+'\n'+album)
        # Actualizo informacion en ventana
        self.ui.lblTitulo.setText(nombre)
        self.ui.lblArtista.setText(artista)
        self.ui.lblAlbum.setText(album)
        self.ui.setWindowTitle("LNMusic - " + nombre)
    
    def abrirArchivo(self):
        '''Abre un archivo de audio'''
        archivo = QtGui.QFileDialog.getOpenFileName(
            self,
            u"Abrir Archivo",
            u"/",
            u"Archivos de Audio (*.mp3 *.wav *.ogg)")
        
        if archivo[1]:
            self.path = archivo[0]
            self.player.setCurrentSource(self.path)
            self.ui.lstListaRep.addItem(self.path)

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

# Creo una aplicacion, le pongo nombre
app = QtGui.QApplication(sys.argv)
app.setApplicationName("LNMusic")
# Ejecuto la clase
rep = Reproductor("graphic.ui", "login.ui")
sys.exit(app.exec_())
