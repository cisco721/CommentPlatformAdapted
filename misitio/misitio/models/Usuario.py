#*********************************************************************************************
#                      Archivo: Usuario.py
#                      -------------------
#   copyright            : (C) 2012 by Developer Group: Jose Francisco
#							de Jesus Perez Vera
#                                                       Armen Djenanian Dertorossian
#							Kristian Cortes
# ********************************************************************************************
# PlatformCommentAdapter. Proyecto de Desarrollo del Software
# ********************************************************************************************
# Descripcion : Archivo que contiene la Clase Usuario
# ********************************************************************************************

import pycassa
from pycassa.pool import ConnectionPool
from pycassa.columnfamily import ColumnFamily
import datetime

class Usuario:
    pass

############################################################
#--------------------- registrarse ------------------------#
#	Procedimiento que permite registrar a un	   #
#	usuario en la base de datos ingresando todos	   #
#	los datos Pertinentes				   #
############################################################
    def registrarse(self): 
        try:
            pool = ConnectionPool('baseDeDatos')
            col_fam = pycassa.ColumnFamily(pool, 'Usuario')
	    resultado = col_fam.get_range(column_start='biografia', column_finish='segundoNombre')
	    for key,columns in resultado:
	        if(key == self.nickName):
	            return 'Error'
	    col_fam.insert (self.nickName, {'password': self.password
	    ,'primerNombre': self.primerNombre
	    ,'segundoNombre': self.segundoNombre
	    ,'primerApellido': self.primerApellido
	    ,'segundoApellido': self.segundoApellido
	    ,'email': self.email
	    ,'fechaNacimiento': self.fechaNacimiento
	    ,'paisOrigen': self.paisOrigen
	    ,'biografia': self.biografia
	    ,'foto': self.foto})
        except Exception:
	    return "FALSE"
	else:
	    return "TRUE"

############################################################
#--------------------- modificarse ------------------------#
#	Procedimiento que permite modificar a un	   #
#	usuario en la base de datos ingresando todos	   #
#	los datos Pertinentes				   #
############################################################
    def modificarse(self):    
        try:
	    pool = ConnectionPool('baseDeDatos')
 	    col_fam = pycassa.ColumnFamily(pool, 'Usuario')	
	    col_fam.insert (self.nickName, {'password': self.password
	    ,'primerNombre': self.primerNombre
	    ,'segundoNombre': self.segundoNombre
	    ,'primerApellido': self.primerApellido
	    ,'segundoApellido': self.segundoApellido
	    ,'email': self.email
	    ,'fechaNacimiento': self.fechaNacimiento
	    ,'paisOrigen': self.paisOrigen
	    ,'biografia': self.biografia
	    ,'foto': self.foto})
        except Exception:
            return "FALSE"
	else:
            return "TRUE"

############################################################
#------------------ Eliminar Usuario ----------------------#
#	Procedimiento que permite eliminar a un usuario    #
#	cuyo nickName, password y token sean validos.      #
#	Una vez confirmada la operacion el usuario es      #
#	borrado automaticamente de la BD		   #
############################################################
    def eliminarUsuario(self):
	try:	
            pool = ConnectionPool('baseDeDatos')
	    col_fam = pycassa.ColumnFamily(pool, 'Usuario')
	    col_fam.remove(self.nickName)
		
	except Exception:
	    return "FALSE"
	else:
	    return "TRUE"

############################################################
#------------------- Validar Usuario ----------------------#
#	Procedimiento que verifica si un usuario esta	   #
#	o no registrado en la base de datos y los datos    #
#	de ingreso son los correctos.			   #
############################################################
    def validarSesion(self,nickName):
        try:
	    pool = ConnectionPool('baseDeDatos')
	    col_fam = pycassa.ColumnFamily(pool, 'Usuario')
	    resultado = col_fam.get(self.nickName,columns=['password'])
            clave = resultado['password']

	    if(self.nickName == nickName) and (clave == self.password):
	        return "TRUE"
	    else:
		return "FALSE"
        except Exception: 
	    return "FALSE"
