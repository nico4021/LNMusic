#! /usr/bin/env python
# -*- coding: utf-8 -*-

from PySide import QtCore, QtGui, QtUiTools
from PySide.phonon import Phonon
import sys, pynotify, time, os
from base import BaseDeDatos


class Reproductor(QtGui.QMainWindow):
    '''Es la clase que gestiona el reproductor'''
    titulo = "LNMusic"
    usuario, contra = None, None
    usuario_y_contra = False
    
    def __init__(self, ui, login, ingresar):
        QtGui.QMainWindow.__init__(self)
        # Contiene los iconos que mas se usan
        self.iconos = {
            "porky": os.path.abspath("img/chanchito.png"),
            "porky-w": QtGui.QIcon("img/chanchito.png"),
            "play": QtGui.QIcon("img/Knob Play.png"),
            "pause": QtGui.QIcon("img/Knob Pause.png"),
            }

        # Inicio pynotify
        pynotify.init("LNMusic")
        self.noti = pynotify.Notification(' ', ' ', self.iconos["porky"])
        
        # Creo el gestor de base de datos
        self.db = BaseDeDatos('db/base.db')
        
        # Cargo el archivo con los elementos graficos
        loader = QtUiTools.QUiLoader()
        self.ingresar = loader.load(ingresar)
        self.login = loader.load(login)
        self.ui = loader.load(ui)

#####
        # Creo un reproductor de tipo musica
        self.player = Phonon.createPlayer(Phonon.MusicCategory)
        self.player.setTickInterval(1000)
        
        # Creo slider del audio
        slider = Phonon.SeekSlider(self)
        slider.setMediaObject(self.player)
        
        self.ui.seekLayout.addWidget(slider)

        # Conecto los eventos
        self.connect(self.ui.btnPlay, QtCore.SIGNAL("clicked()"), self.play)
        self.connect(self.ui.btnAdelantar, QtCore.SIGNAL("clicked()"), self.siguiente)
        self.connect(self.ui.btnAtrasar, QtCore.SIGNAL("clicked()"), self.anterior)
        self.connect(self.ui.btnAdd, QtCore.SIGNAL("clicked()"), self.abrirArchivo)
        self.connect(self.ui.lstListaRep, QtCore.SIGNAL("itemSelectionChanged()"), self.cambiaSeleccionLst)
        self.connect(self.ui.lstListas, QtCore.SIGNAL("itemSelectionChanged()"), self.cambiaSeleccionLst2)
        self.connect(self.ui.btnDelete, QtCore.SIGNAL("clicked()"), self.eliminarCancion)
        self.connect(self.ui.btnSearch, QtCore.SIGNAL("clicked()"), self.filtrar)
        self.connect(self.ui.actionNuevo_Perfil, QtCore.SIGNAL("triggered()"), self.nuevoPerfil)
        self.connect(self.ui.actionCerrar_sesion, QtCore.SIGNAL("triggered()"), self.cerrarSesion)
        self.connect(self.ui.actionImportar, QtCore.SIGNAL("triggered()"), self.abrirArchivo)
        self.connect(self.ui.actionEliminar_Perfil, QtCore.SIGNAL("triggered()"), self.eliminarPerfil)
        self.connect(self.ui.actionCerrar, QtCore.SIGNAL("triggered()"), self.ui.close)
        self.connect(self.ui.actionGuardar, QtCore.SIGNAL("triggered()"), self.guardarLista)
        self.connect(self.ui.actionEliminar_Lista, QtCore.SIGNAL("triggered()"), self.eliminarLista)
        self.connect(self.ui.actionNueva_Lista, QtCore.SIGNAL("triggered()"), self.nuevaLista)
        self.player.metaDataChanged.connect(self.metaData)
        self.player.stateChanged.connect(self.state)
        self.player.tick.connect(self.tick)
        self.player.aboutToFinish.connect(self.aboutToFinish)
        
        self.ui.setWindowIcon(self.iconos["porky-w"])
#####

        # Abro el login
        self.ingresar.show()
        self.ingresar.cmbUsuario.setFocus()
        
        # Agrego todos los usuarios a la lista de usuarios
        self.ingresar.cmbUsuario.addItems(self.db.obtenerUsuarios())
        
        def hay_usuario_y_contra():
            # Obtengo usuario y contraseña
            self.usuario = self.ingresar.cmbUsuario.currentText()
            self.contra = self.ingresar.txtContra.text()

            # Si faltan datos
            if not(self.usuario and self.contra):
                # No se habilita el boton ingresar
                self.ingresar.btnIngresar.setEnabled(False)
            # Si se llenaron los todos los campos
            else:
                # Se habilita el ingreso
                self.ingresar.btnIngresar.setEnabled(True)
        
        def ingresar():
            # Busco en la base de datos al perfil con dicho nombre de usuario
            perfil = self.db.obtenerPerfil(self.usuario)
            
            # Si la contraseña es incorrecta
            if self.contra != perfil[0][1]:
                # Muestro un error
                QtGui.QMessageBox.critical(self, 'Error!!!', u'Contraseña incorrecta.')

            else:
                # Cierra el dialogo
                self.ingresar.close()
                self.ingresar.txtContra.setText("")
                self.ingresar.cmbUsuario.setFocus()
                # Inicia el reproductor de musica
                self.iniciar_reproductor()
        
        # Eventos para verificar si se completaron los campos
        self.ingresar.cmbUsuario.currentIndexChanged.connect(hay_usuario_y_contra)
        self.ingresar.txtContra.textChanged.connect(hay_usuario_y_contra)
        # Evento para ingresar
        self.ingresar.btnIngresar.clicked.connect(ingresar)
        self.ingresar.btnNuevo.clicked.connect(self.nuevoPerfilLog)


    def iniciar_reproductor(self):
        # Abro la ventana
        self.ui.show()
        self.titulo = self.titulo + " (" + self.usuario + ")"
        self.ui.setWindowTitle(self.titulo)

        self.ui.lstListas.clear()
        self.ui.lstListaRep.clear()

        for i in self.db.obtenerListas(self.usuario):
            self.ui.lstListas.addItem(i)

        self.ui.lblListaActual.setText(u'Mi música')

        for i in self.db.obtenerCanciones(u'Mi música', self.usuario):
            self.ui.lstListaRep.addItem(i)

    def tick(self, time):
        '''Se encarga de llevar la cuenta del tiempo transcurrido'''
        displayTime = QtCore.QTime(0, (time / 60000) % 60, (time / 1000) % 60)
        self.ui.musicTime.setText(displayTime.toString('mm:ss'))

    def state(self, estado):
        if estado == Phonon.State.PlayingState:
            self.noti.show()
            # Cambia el icono
            self.ui.btnPlay.setIcon(self.iconos["pause"])
        elif estado == Phonon.State.StoppedState:
            # Cambia el icono
            self.ui.btnPlay.setIcon(self.iconos["play"])
            # Actualizo informacion en ventana
            self.ui.lblTitulo.setText('-')
            self.ui.lblArtista.setText('-')
            self.ui.lblAlbum.setText('-')
        elif estado == Phonon.State.PausedState:
            # Cambia el icono
            self.ui.btnPlay.setIcon(self.iconos["play"])

    def aboutToFinish(self):
        self.player.clearQueue()

    def anterior(self):
        self.player.seek(0)

    def siguiente(self):
        self.player.seek(10000000)

    def play(self):
        '''Reproduce un archivo'''
        # Estado del reproductor
        estado = self.player.state()
        # Si esta reproducciendo
        if estado == Phonon.State.PlayingState:
            # Pausa la reproduccion
            self.player.pause()
        elif estado == Phonon.State.PausedState:
            self.player.play()
        else:
            canciones = self.ui.lstListaRep.selectedItems()
            listaRep = []
            
            if canciones:
                for i in canciones:
                    if i is canciones[0]:
                        self.player.setCurrentSource(i.text())
                    else:
                        listaRep.append(i.text())

                self.player.setQueue(listaRep)
                # Lo reproduce
                self.player.play()

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

        # Actualizo notificacion
        self.noti.update(nombre, artista+'\n'+album, self.iconos["porky"])
        # Actualizo informacion en ventana
        self.ui.lblTitulo.setText(nombre)
        self.ui.lblArtista.setText(artista)
        self.ui.lblAlbum.setText(album)
        self.ui.setWindowTitle(self.titulo + " - " + nombre)
    
    def abrirArchivo(self):
        '''Abre un archivo de audio'''
        archivo = QtGui.QFileDialog.getOpenFileNames(
            self,
            u"Abrir Archivo",
            u"/",
            u"Archivos de Audio (*.mp3 *.wav *.ogg *.flac *.mp4 *.m4a)")
        
        if archivo[1]:
            path = archivo[0]
            for i in path:
                self.ui.lstListaRep.addItem(i)
            

    def nuevoPerfilLog(self):
        self.nuevoPerfil()
        
        # Vacio los usuarios
        for i in range(self.ingresar.cmbUsuario.count()):
            self.ingresar.cmbUsuario.removeItem(0)
            
        # Agrego todos los usuarios a la lista de usuarios
        self.ingresar.cmbUsuario.addItems(self.db.obtenerUsuarios())

    def nuevoPerfil(self):
        '''Crea un nuevo perfil con los datos ingresados'''
        # Cambio el titulo del dialog
        self.login.setWindowTitle(self.titulo + " - Nuevo perfil")
        
        # Limpio los campos
        self.login.txtPass.setText('')
        self.login.txtUsuario.setText('')
        self.login.txtUsuario.setFocus()
        
        # Lo ejecuto
        if self.login.exec_():
            usuario = self.login.txtUsuario.text()
            contra = self.login.txtPass.text()
            # Si no se ha ingresado alguno de los campos
            if not(usuario and contra):
                # Muestro una advertencia
                QtGui.QMessageBox.warning(self.login, 'Advertencia!!!', u'No se han ingresado todos los campos. Por favor, elija un usuario y una contraseña para su nuevo perfil.')
            else:
                try:
                    # Creo un nuevo perfil en la base de datos
                    self.db.nuevoPerfil(usuario, contra)
                    # Muestro un mensaje de exito
                    QtGui.QMessageBox.information(self.login, 'Exito!!!', u'Se ha creado un nuevo perfil exitosamente.')
                # Si hay un error, (nombre de usuario repetido)
                except:
                    # Muestro una advertencia
                    QtGui.QMessageBox.warning(self.login, 'Advertencia!!!', 'Ya existe un perfil con ese nombre de usuario. Pruebe ingresando un usuario diferente.')
        
        # Limpio los campos
        self.login.txtPass.setText('')
        self.login.txtUsuario.setText('')
        
        self.login.txtUsuario.setFocus()

    def cerrarSesion(self):
        # Cierro la ventana
        self.ui.close()
        self.titulo = "LNMusic"
        # Abro el login
        self.ingresar.show()
        
        # Vacio los usuarios
        for i in range(self.ingresar.cmbUsuario.count()):
            self.ingresar.cmbUsuario.removeItem(0)
            
        # Agrego todos los usuarios a la lista de usuarios
        self.ingresar.cmbUsuario.addItems(self.db.obtenerUsuarios())

    def eliminarPerfil(self):
        # Pido una confirmacion para eliminar perfil
        msj = QtGui.QMessageBox.warning(self.ui, u'¿Eliminar perfil?', u'¿Esta seguro que desea eliminar su perfil? Perdera todos sus datos, listas de reproduccion.', QtGui.QMessageBox.Cancel | QtGui.QMessageBox.Ok, QtGui.QMessageBox.Cancel)
        
        # Si se acepto
        if msj == QtGui.QMessageBox.Ok:
            self.db.borrarPerfil(self.usuario)
            # Muestro un mensaje de exito
            QtGui.QMessageBox.information(self.login, 'Exito!!!', u'El perfil se ha eliminado correctamente.')
            # Cierro el reproductor
            self.ui.close()

    def cambiaSeleccionLst(self):
        '''Habilita o deshabilita el boton para eliminar canciones de la lista'''
        if self.ui.lstListaRep.selectedItems():
            self.ui.btnDelete.setEnabled(True)
        else:
            self.ui.btnDelete.setEnabled(False)

    def cambiaSeleccionLst2(self):
        selec = self.ui.lstListas.selectedItems()

        if selec:
            actual = selec[0].text()
            self.ui.lblListaActual.setText(actual)
            self.ui.lstListaRep.clear()

            for i in self.db.obtenerCanciones(actual, self.usuario):
                self.ui.lstListaRep.addItem(i)

    def eliminarCancion(self):
        '''Elimina las canciones seleccionadas'''
        for i in self.ui.lstListaRep.selectedItems():
            self.ui.lstListaRep.takeItem(self.ui.lstListaRep.row(i))

    def guardarLista(self):
        listas = self.db.obtenerListas(self.usuario)
        actual = self.ui.lblListaActual.text()
        count = self.ui.lstListaRep.count()
        canciones = []

        if not count:
            # Muestro una advertencia
            QtGui.QMessageBox.warning(self.ui, 'No hay canciones', u'No hay canciones para agregar a su lista de reproduccion.')

        else:
            for i in range(count):
                canciones.append(self.ui.lstListaRep.item(i))

            if not(actual in listas):
                self.db.nuevaLista(actual, self.usuario)

            self.db.agregarCanciones(canciones, actual, self.usuario)

            # Muestro un mensaje informativo
            QtGui.QMessageBox.information(self.ui, 'Exito!!!', u'Su lista de reproduccion '+actual+' se ha guardado con exito.')

    def eliminarLista(self):
        actual = self.ui.lstListas.selectedItems()
        
        if actual[0].text() == u'Mi música':
            QtGui.QMessageBox.critical(self.ui, 'Error!!!', u'No se puede eliminar la lista de reproduccion '+actual[0].text()+'.')
        elif actual:
            # Pido una confirmacion para eliminar lista
            msj = QtGui.QMessageBox.warning(self.ui, u'¿Eliminar lista de reproduccion?', u'¿Esta seguro que desea eliminar la lista de reproduccion '+actual[0].text()+'?', QtGui.QMessageBox.Cancel | QtGui.QMessageBox.Ok, QtGui.QMessageBox.Cancel)
            
            # Si se acepto
            if msj == QtGui.QMessageBox.Ok:
                self.db.borrarLista(actual[0].text(), self.usuario)
                self.ui.lstListas.takeItem(self.ui.lstListas.row(actual[0]))
                # Muestro un mensaje de exito
                QtGui.QMessageBox.information(self.ui, 'Exito!!!', u'La lista de reproduccion se ha eliminado correctamente.')

        else:
            QtGui.QMessageBox.critical(self.ui, 'Error!!!', u'Debe seleccionar una lista de reproduccion.')

    def nuevaLista(self):
        listas = self.db.obtenerListas(self.usuario)
        text, ok = QtGui.QInputDialog.getText(self, 'Nueva lista', 'Nombre de la lista:')

        if ok:
            if text and not(text in listas):
                self.db.nuevaLista(text, self.usuario)
                self.ui.lstListas.addItem(text)
                QtGui.QMessageBox.information(self.ui, 'Exito', u'Lista '+text+' creada con exito.')
            else:
                QtGui.QMessageBox.critical(self.ui, 'Error!!!', u'Debe ingresar un nombre valido.')

    def filtrar(self):
        filtro = self.ui.leSearch.text()
        items = self.ui.lstListaRep.findItems(filtro, QtCore.Qt.MatchContains)
        lista = []

        for i in range(len(items)):
            lista.append(items[i].text())

        self.ui.lstListaRep.clear()
        
        for i in lista:
            self.ui.lstListaRep.addItem(i)


# Creo una aplicacion, le pongo nombre
app = QtGui.QApplication(sys.argv)
app.setApplicationName("LNMusic")
# Ejecuto la clase
rep = Reproductor("graphic.ui", "nuevo.ui", "ingresar.ui")
sys.exit(app.exec_())
