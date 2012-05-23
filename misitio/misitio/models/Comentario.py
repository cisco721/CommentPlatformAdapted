#*********************************************************************************************
#                      Archivo: Comentario.py
#                      -------------------
#   copyright            : (C) 2012 by Developer Group: Jose Francisco
#							de Jesus Perez Vera
#                                                       Armen Djenanian Dertorossian
#							Kristian Cortes
# ********************************************************************************************
# PlatformCommentAdapter. Proyecto de Desarrollo del Software
# ********************************************************************************************
# Descripcion : Archivo que contiene la Clase Comentario
# ********************************************************************************************

import pycassa
from pycassa.pool import ConnectionPool
from pycassa.columnfamily import ColumnFamily
import smtplib

class Comentario:
    pass

############################################################
#--------------- registrar Comentario ---------------------#
#	Rutina que se encarga de registrar en la BD	   #
#	un comentario de un usuario. Este procedimiento	   #
#       es llamado desde la vista viewsComentario.py       #
############################################################
    def registrarComentario (self,etiquetas):
        try:
            pool = ConnectionPool('baseDeDatos')
	    col_fam = pycassa.ColumnFamily(pool,'Comentario')
	    elId = generarIdComentario()
	    if(elId != "FALSE"):
	        self.idComentario = elId 
	        col_fam.insert (self.idComentario, {'nickName': self.nickName
						   ,'texto': self.texto 
                                                   ,'adjunto': self.adjunto
						   ,'admiteRespuesta': self.admiteRespuesta
						   ,'fecha': self.fecha
						   ,'token': self.token})
	        if (etiquetas != " "):
		   agregarEtiquetas(etiquetas,self.idComentario,self.nickName)
	    else:
	        return "FALSE"
        except Exception:
            return "FALSE"
        else:
            return "TRUE"
	
    def responderComentario(self):
        try:
	    pool = ConnectionPool('baseDeDatos')
	    col_fam = pycassa.ColumnFamily(pool,'Comentario')
	    elId = generarIdComentario()
	    if (elId != "FALSE"):
                self.idRespuesta = elId 
	        col_fam.insert (self.idRespuesta, {'nickName': self.nickName
						 ,'idComentario': self.idComentario
						 ,'usuarioRespuesta': self.usuarioRespuesta
						 ,'texto': self.texto
						 ,'adjunto': self.adjunto
						 ,'fecha': self.fecha
						 ,'token': self.token})
	except Exception:
	    return "FALSE"
	else:
	    return "TRUE"

############################################################
#-------------------- Admite Respuesta --------------------#
    def admitirRespuesta(self,idComentario):
	try:	
	    pool = ConnectionPool('baseDeDatos')
	    col_fam = pycassa.ColumnFamily(pool, 'Comentario')
	    resultado = col_fam.get(idComentario,columns=['admiteRespuesta']) 
	    admiteRespuesta = resultado['admiteRespuesta']
	    if (admiteRespuesta == "True"):
	        return "TRUE"
	    else:
		return "FALSE"
	except Exception:
	    return "FALSE"
	else:
	    return "TRUE"

##########################################################################
#-------------------- Notificar respuesta comentario --------------------#
    def notificarRespuestaComentario(self,usuarioRespuesta):
        try:
	    pool = ConnectionPool('baseDeDatos')
	    col_fam = pycassa.ColumnFamily(pool, 'Usuario')
	    resultado = col_fam.get(usuarioRespuesta,columns=['email']) 
	    emailDestinatario = resultado['email']
	    De = "equipoafkdesarrollo"
	    texto = "La Plataforma de intercambio de mensajes PlataformCommentAdapted le informa que ud ha recibido una respuesta a un comentario\n----------------------------------------------------------------------------------------------------------------\nPara mayor informacion inicie sesion con su cuenta y mantengase siempre comunicado(a) \n\n 								                    Atentamente:\n Equipo de PlataformCommentAdapted"
			
            server = smtplib.SMTP("smtp.gmail.com:587")
	    server.starttls()
	    server.login("equipoafkdesarrollo", "kristian1234")
	    server.sendmail(De, emailDestinatario, texto)
	    server.quit()

	except Exception:
	     return "FALSE"
	else:
             return "TRUE"

###############################################################
#-------------------- Eliminar Comentario --------------------#
    def eliminarComentario(self,idComentario):
        try:	
	    pool = ConnectionPool('baseDeDatos')
	    col_fam = pycassa.ColumnFamily(pool, 'Comentario')
	    try:
	        resultado = col_fam.get(idComentario,columns=['nickName'])
	    except Exception:
	        return "ERROR"
	    nickName = resultado ['nickName']
	    if (self.nickName == nickName): 
		col_fam.remove(str(idComentario))
	    else:
		return 'Error'
	except Exception:
	    return "FALSE"
	else:
	    return "TRUE"

############################################################
#----------------- registrar me Gusta----------------------#
    def ponerMeGusta(self):
        try:
	    pool = ConnectionPool('baseDeDatos')
	    col_fam = pycassa.ColumnFamily(pool, 'Gusto')
	    resultado = col_fam.get_range(column_start='gusto', column_finish='nickName')
	    for key,columns in resultado:
	        if(columns['nickName'] == self.nickName and columns['idComentario'] == self.idComentario):
	            if(columns['gusto']=='TRUE'):
		        return 'FALSE'
		    elif(columns['gusto']=='FALSE'):
		        col_fam.insert (key, {'idComentario': self.idComentario,'nickName': self.nickName,'gusto':'TRUE'})
		        return'CAMBIO'
		   
	    elId = generarIdGusta()
	    if(elId != "FALSE"):
	        self.idRespuesta = elId
	        col_fam.insert (self.idRespuesta, {'idComentario': self.idComentario,'nickName': self.nickName,'gusto':'TRUE'})
	        return 'TRUE'
		          
	except Exception:
	    return "FALSE"
	else:
	    return "TRUE"

###############################################################
#----------------- registrar no me Gusta----------------------#
    def ponerNoMeGusta(self):
        try:
	    pool = ConnectionPool('baseDeDatos')
	    col_fam = pycassa.ColumnFamily(pool, 'Gusto')
	    resultado = col_fam.get_range(column_start='gusto', column_finish='nickName')
	    for key,columns in resultado:
	        if(columns['nickName'] == self.nickName and columns['idComentario'] == self.idComentario):
		    if(columns['gusto']=='FALSE'):
		        return 'FALSE'
		    elif(columns['gusto']=='TRUE'):
		        col_fam.insert (key, {'idComentario': self.idComentario,'nickName': self.nickName,'gusto':'FALSE'})
		        return'CAMBIO'
		   
	    elId = generarIdGusta()
	    if(elId != "FALSE"):
	        self.idRespuesta = elId
		col_fam.insert (self.idRespuesta, {'idComentario': self.idComentario,'nickName': self.nickName,'gusto':'FALSE'})
		return 'TRUE'
		          
	except Exception:
	    return "FALSE"
	else:
	    return "TRUE"

############################################################
#----------------- validar Comentario----------------------#
    def ValidarComentario(self,idComentario):
        try:
	    pool = ConnectionPool('baseDeDatos')
	    col_fam = pycassa.ColumnFamily(pool, 'Comentario')
	    resultado = col_fam.get(idComentario,columns=['nickName'])
	    return 'TRUE'
	except Exception:
	    return "FALSE"

############################################################
#-------------------- Lista  Comentario--------------------#
    def listaComentario(nickName):
	pool = ConnectionPool('baseDeDatos')
	col_fam = pycassa.ColumnFamily(pool, 'Comentario')
	resultado = col_fam.get_range(column_start='adjunto', column_finish='token')
	encontrado = False
	listaDeComentarios = []
	for key,columns in resultado:
	    if columns['nickName'] == nickName:
	        listaDeComentarios.append(key+":"+columns['nickName']+":"+columns['texto']+":"+columns['token']+":"+columns['adjunto'])
		encontrado = True

	if(encontrado):
	    return listaDeComentarios
	else:
	    return "FALSE"

############################################################
#-------------------- Lista  Respuesta --------------------#
    def listaRespuesta(usuarioRespuesta,idComentario):
	
	pool = ConnectionPool('baseDeDatos')
	col_fam = pycassa.ColumnFamily(pool, 'Comentario')
	resultado = col_fam.get_range(column_start='adjunto', column_finish='usuarioRespuesta')
	encontrado = False
	listaDeComentarios = []
	for key,columns in resultado:
	    if len(columns)>6 and columns['usuarioRespuesta'] == usuarioRespuesta and columns['idComentario'] == idComentario:
	        listaDeComentarios.append(columns['usuarioRespuesta']+":"+columns['nickName']+":"+columns['texto'])
		encontrado = True
	if(encontrado):
	    return listaDeComentarios
	else:
	    return "FALSE"

############################################################
#----------------- Lista Etiqueta--------------------------#
    def listaEtiquetas(nombreEtiqueta):
	
	pool = ConnectionPool('baseDeDatos')
	col_fam = pycassa.ColumnFamily(pool, 'Etiqueta')
	resultado = col_fam.get_range(column_start='idComentario', column_finish='nombreEtiqueta')
	encontrado = False
	listaDeDatos = []
	for key,columns in resultado:
	    if columns['nombreEtiqueta'] == nombreEtiqueta:
	        listaDeDatos.append(columns['idComentario']+":"+columns['nickName'])
		encontrado = True

	if(encontrado):
	    return listaDeDatos
	else:
	    return "FALSE"

############################################################
#------------ Lista comentarios con etiquetas--------------#
    def listarComentariosConEtiqueta(idComentario,nickName):
	try:    
	    listaDeComentarios = ' '
	    pool = ConnectionPool('baseDeDatos')
	    col_fam = pycassa.ColumnFamily(pool, 'Comentario')
	    resultado = col_fam.get(idComentario,columns=['nickName','texto'])
	    listaDeComentarios = resultado['texto']+":"
	except Exception: 
	    return " "
	else:
	    return listaDeComentarios

############################################################
#-----------------------Contar me gusta--------------------#
    def contarMeGusta(idComentario):
	try:	
	    meGustan = 0
	    pool = ConnectionPool('baseDeDatos')
	    col_fam = pycassa.ColumnFamily(pool,'Gusto')
	    resultado = col_fam.get_range(column_start='gusto', column_finish='nickName')
	    for key,columns in resultado:
	        if(columns['idComentario'] == idComentario and columns['gusto'] == "TRUE" ):
		    meGustan = meGustan + 1		  
		
	except Exception: 
		return "FALSE"
	else:
		return meGustan

############################################################
#--------------------Contar no me gusta--------------------#
    def contarNoMeGusta(idComentario):
	try:	
	    noMeGustan = 0
	    pool = ConnectionPool('baseDeDatos')
	    col_fam = pycassa.ColumnFamily(pool,'Gusto')
	    resultado = col_fam.get_range(column_start='gusto', column_finish='nickName')
	    for key,columns in resultado:
	        if(columns['idComentario'] == idComentario and columns['gusto'] == "FALSE" ):
		    noMeGustan = noMeGustan + 1
	except Exception: 
		return "FALSE"
	else:
		return noMeGustan



############################################################
#----------------- GenerarId Comentario--------------------#
def generarIdComentario():
    vacio = True
    try:
        pool = ConnectionPool('baseDeDatos')
        col_fam = pycassa.ColumnFamily(pool,'Comentario')
        resultado = col_fam.get_range(column_start='nickName', column_finish='texto')
        arreglo = []
        for key,columns in resultado:
            arreglo.append(int(key)+1)
	    vacio = False
	lista = sorted(arreglo,reverse=True)

    except Exception:
        return "FALSE"
    else:
	if vacio == True:
	    return '1'
	else:
	    nuevoId = str(lista[0])
	    return nuevoId

############################################################
#----------------- GenerarId Gusta--------------------#
def generarIdGusta():
    vacio = True
    try:
	pool = ConnectionPool('baseDeDatos')
	col_fam = pycassa.ColumnFamily(pool,'Gusto')
	resultado = col_fam.get_range(column_start='idComentario', column_finish='nickName')
	arreglo = []
        for key,columns in resultado:
	    arreglo.append(int(key)+1)
	    vacio = False
        lista = sorted(arreglo,reverse=True)
    except Exception:
	return "FALSE"
    else:
	if vacio == True:
	    return '1'
	else:
	    nuevoId = str(lista[0])
	    return nuevoId

############################################################
#----------------- Generar Id de Etiqueta------------------#
def generarIdEtiqueta():
    vacio = True
    try:
        pool = ConnectionPool('baseDeDatos')
        col_fam = pycassa.ColumnFamily(pool,'Etiqueta')
	resultado = col_fam.get_range(column_start='idComentario', column_finish='nickName')
	arreglo = []
	for key,columns in resultado:
	    arreglo.append(int(key)+1)
	    vacio = False

	listaIdEtiqueta = sorted(arreglo,reverse=True)

    except Exception:
        return "FALSE"
    else:
        if vacio == True:
            return '1'
        else:
            nuevoId = str(listaIdEtiqueta[0])
	    return nuevoId

def agregarEtiquetas(etiquetas,idComentario,nickName):

    pool = ConnectionPool('baseDeDatos')
    col_fam = pycassa.ColumnFamily(pool,'Etiqueta')
    arreglo = etiquetas.split(',')
    i = 0
    while i < len(arreglo):
        idEtiqueta = generarIdEtiqueta()
        if idEtiqueta != "FALSE":
	    idEtiqueta = str(idEtiqueta)
	    nombreEtiqueta = arreglo[i] 
	    col_fam.insert (idEtiqueta, {'nombreEtiqueta': nombreEtiqueta,'idComentario': idComentario,'nickName':nickName})
        i = i + 1

