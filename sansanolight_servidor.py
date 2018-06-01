#!/usr/bin/env python
# -*- coding: utf-8 -*-

#-------------------------------|
#     MODULOS NECESARIOS        |
#-------------------------------|

import socket
import pigpio

#-------------------------------|
#          FUNCIONES            |
#-------------------------------|

def control_leds(colores):

    #Asociamos cada canal a un puerto
    RED = 22
    GREEN = 17
    BLUE = 24
    r = int(colores[0])
    g = int(colores[1])
    b = int(colores[2])

    #Cambiamos el brillo del canal de acuerdo a los parametros entregados
    setLights(RED,r)
    setLights(GREEN,g)
    setLights(BLUE,b)


def setLights(pin, brightness):
    
    global pi
    
    realBrightness = int(int(brightness) * (float(150) / 255.0))
    pi.set_PWM_dutycycle(pin, realBrightness)
    

#-------------------------------|
#           PROGRAMA            |
#-------------------------------|


#Iniciamos variable socket-servidor para trabajar con el socket y esperamos la conexion.
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("", 9993))
s.listen(1)

#Iniciamos la variable que controla los puertos gpio
pi = pigpio.pi()
 
#Iniciamos variable socket-cliente para recibir los datos
print 'Esperando conexion ...'
sc, addr = s.accept()
 
 
while True:
 
    #Recibimos los datos enviados
    recibido = sc.recv(1024)
 
    #Si el mensaje recibido es la palabra close se cierra la aplicacion
    if recibido == "close":
        break
 
    #Devolvemos el mensaje al cliente
    sc.send(recibido)

    #Iniciamos el control de leds
    colores = recibido.strip()
    colores = colores.split(',')
    if len(colores)==3:
        if int(colores[0])<256 and int(colores[1])<256 and int(colores[2])<256:
            control_leds(colores)
    
    
print "Adios."
 
#Cerramos la instancia del socket cliente y servidor
sc.close()
s.close()
