#*********************************************************************************************
#                      Archivo: Token.py
#                      -------------------
#   copyright            : (C) 2012 by Developer Group: Jose Francisco
#							de Jesus Perez Vera
#                                                       Armen Djenanian Dertorossian
#							Kristian Cortes
# ********************************************************************************************
# PlatformCommentAdapter. Proyecto de Desarrollo del Software
# ********************************************************************************************
# Descripcion : Archivo que contiene la Clase Token
# ********************************************************************************************

import datetime
import time
import pycassa
from pycassa.pool import ConnectionPool
from pycassa.columnfamily import ColumnFamily

class Token:
    pass

############################################################
#--------------------- Validar Token ----------------------#
#	Procedimiento que se encarga de validar		   #
#	que un mismo IP maneje un solo token a la vez      #
############################################################

    def validarToken(self):
    	try:
	    now = datetime.datetime.now()
	    pool = ConnectionPool('baseDeDatos')
	    col_fam = pycassa.ColumnFamily(pool, 'Token')
	    resultado = col_fam.get(self.token,columns=['idToken','ip','fecha','nickName'])
            clave = resultado['idToken']
            ip = resultado['ip']
	    nowToken = resultado['fecha']
	    nickName = resultado['nickName']
	    if (ip==self.ip) and(clave == self.token) and (nickName == self.nickName):
	         nowToken2 = resultado['fecha'].split(".")
		 nowToken =datetime.datetime(*time.strptime(nowToken2[0],'%Y-%m-%d %H:%M:%S')[0:6])
		 diferenciaToken = now - nowToken
		 horas = str(diferenciaToken).split(":")
		 minutos = int(horas[1])
		 if (horas[0]=="0") and (minutos<=4):
	              return "TRUE"
	         else:
		      return "Error"
	    else:
		 return "FALSE"
        except Exception:
	    return "FALSE"
	else:
	    return "TRUE"

############################################################
#-------------------- Insertar Token ----------------------#
#	Rutina que se encarga de insertar un token	   #
#	valido en la base de datos, con todos los	   #
#	datos pertinentes				   #
############################################################
    def insertarToken(self):
	try:	
	    now = datetime.datetime.now()
	    pool = ConnectionPool('baseDeDatos')	
	    col_fam = pycassa.ColumnFamily(pool, 'Token')
	    elId = generarIdToken()
	    if(elId != "FALSE"):
	    	col_fam.insert (elId, {'ip': self.ip,'fecha': str(now) ,'nickName': self.nickName, 'accion': 'Generar Token', 'idToken': elId})
        except Exception:
	    return "FALSE"
	else:
	    return elId

############################################################
#-------------------- Tiene Token -------------------------#
#	Rutina que se encarga de validar si un usuario     #
#	tiene un token vigente o no. De acuerdo a la 	   #
#	respuesta "TRUE" o "FALSE" entonces se decide      #
#	crear uno nuevo o indicar un mensaje de error	   #
#	advirtiendo que el usuario ya tiene un token	   #
#	valido en su maquina				   #
############################################################
    def tieneToken(self):
        try:    
	    pool = ConnectionPool('baseDeDatos')
	    col_fam = pycassa.ColumnFamily(pool, 'Token')
	    resultado = col_fam.get_range(column_start='accion', column_finish='nickName')
            for key,columns in resultado:	 
                 nickName = columns['nickName']
                 ip = columns ['ip']
		 nowToken = columns ['fecha']
						
	         if (nickName == self.nickName and ip == self.ip):
	            nowToken2 = columns['fecha'].split(".")
                    nowToken = datetime.datetime(*time.strptime(nowToken2[0],'%Y-%m-%d %H:%M:%S')[0:6])
		    now = datetime.datetime.now()
		    diferenciaToken = now - nowToken
		    horas = str(diferenciaToken).split(":")	   
		    minutos = int(horas[1])
		   
	            if (horas[0]=="0") and (minutos<=4):
		        return "TRUE"
			
        except Exception:
	    return "TRUE"
	else:
	    return "FALSE"

############################################################
#--------------------- GenerarId Token --------------------#
#	Rutina que genera un id de Token para    	   #
#	luego insertarlo en la BD de forma secuencial	   #
#	con un numero entero a partir del entero 1.	   #
############################################################
def generarIdToken():
    vacio = True
    try:
	pool = ConnectionPool('baseDeDatos')
	col_fam = pycassa.ColumnFamily(pool,'Token')
	resultado = col_fam.get_range(column_start='accion', column_finish='nickName')
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
