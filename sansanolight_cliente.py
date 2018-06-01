#!/usr/bin/env python
# -*- coding: cp1252 -*-
#--------------------------------------------|
#             MODULOS NECESARIOS             |
#--------------------------------------------|

from Tkinter import *
from colorthief import ColorThief
import cv2
import numpy as np
import time, threading
import pyscreenshot as ImageGrab
import socket

#--------------------------------------------|
#                FUNCIONES                   |
#--------------------------------------------|

def capturando_pantalla():

    global s
    
    if correr and conexion:

        #Leemos la pantalla y la guardamos en una variable
        ImageGrab.grab_to_file('captura.png')
        

        #if modo.get() == 2:

        #Cargamos la pantalla con el modulo ColorThief para ver color dominante
        pantalla = ColorThief('captura.png')

        #Obteniendo color predominante
        color_dominante = pantalla.get_color(quality=10)
        
        #Enviando color predominante a raspberry
        s.send(str(color_dominante[0])+','+str(color_dominante[1])+','+str(color_dominante[2]))

        """elif modo.get() == 1:

            #Cargamos la pantalla con el modulo CV2 para obtener colores laterales y superiores
            pantalla = cv2.imread('captura.png')

            #Abrimos archivo de texto donde guardaremos la informacion
            archivo = open('archivo_luces.txt', 'w')

            #Obtenemos la informacion de pantalla y calculamos medidas de cada region
            ancho_pantalla = pantalla.shape[1]
            alto_pantalla = pantalla.shape[0]
            region_lateral = int(luces_laterales.get())
            region_superior = int(luces_superiores.get())
            ancho = int(ancho_pantalla/region_superior)
            alto = int(alto_pantalla/region_lateral)

            #Se construye cada region lateral y se obtiene su informacion
            for k in xrange(region_lateral):
                mask_izquierda = np.zeros((alto_pantalla,ancho_pantalla,1), np.uint8)
                mask_derecha = np.zeros((alto_pantalla,ancho_pantalla,1), np.uint8)

                for i in xrange(alto):
                    for j in xrange(ancho):
                        mask_izquierda[alto*k+i][j] = 1
                        mask_derecha[alto*k+i][ancho_pantalla-j-1] = 1
            
                valor_izquierda = cv2.mean(pantalla, mask=mask_izquierda)
                valor_derecha = cv2.mean(pantalla, mask=mask_derecha)
                ri,gi,bi,_ = map(int,valor_izquierda)
                rd,gd,bd,_ = map(int,valor_derecha)
                archivo.write(str(k+1)+'-i: '+str(ri)+','+str(gi)+','+str(bi)+'\n')
                archivo.write(str(k+1)+'-d: '+str(rd)+','+str(gd)+','+str(bd)+'\n')

            for k in xrange(region_superior):
                mask_superior = np.zeros((alto_pantalla,ancho_pantalla,1), np.uint8)

                for i in xrange(alto):
                    for j in xrange(ancho):
                        mask_superior[i][ancho*k+j] = 1

                valor_superior = cv2.mean(pantalla, mask=mask_superior)
                rs,gs,bs,_ = map(int,valor_superior)
                archivo.write(str(k+1)+'-s: '+str(rs)+','+str(gs)+','+str(bs)+'\n')

            archivo.close()
            ordenar_archivo()"""

    if conexion == 'close':
        s.send('close')
        s.close()
        pass
        
    v.after(10, capturando_pantalla)

def ordenar_archivo():

    #Llamamos a la función global s
    global s

    archivo = open('archivo_luces.txt' , 'r')

    lista_der = []
    lista_izq = []
    lista_arr = []

    for linea in archivo:
    
        linea = linea.strip().split(': ')
        numero, luz = linea[0].split('-')
    
        if luz == 'i':
            lista_izq.append((numero,linea[1]))     
        elif luz == 'd':
            lista_der.append((numero,linea[1]))
        else:
            lista_arr.append((numero,linea[1]))

    archivo.close()
    c = 1

    for i in lista_izq:
        escribir = str(c)+'-'+str(i[1])+'\n'
        c += 1
        s.send(escribir)
    
    for i in lista_arr:
        escribir = str(c)+'-'+str(i[1])+'\n'
        c += 1
        s.send(escribir)
    
    for i in lista_der:
        escribir = str(c)+'-'+str(i[1])+'\n'
        c += 1
        s.send(escribir)

def iniciar_programa():
    global correr
    global conexion
    correr = True
    conexion = True

def detener_programa():
    global correr
    global conexion
    correr = False
    conexion = 'close'

#--------------------------------------------|
#              CREANDO PROGRAMA              |
#--------------------------------------------|

correr = False
conexion = False
s = socket.socket()
#"192.168.43.46"
s.connect(("192.168.43.46", 9999))

#Creando ventana
v = Tk()
v.geometry("450x40")
v.title("SANSANOLIGHT V.2.0")
app = Frame(v)
app.grid()

#Variables que controlan la ejecucion del programa
luces_laterales = StringVar()
luces_laterales.set('10')
luces_superiores = StringVar()
luces_superiores.set('15')
modo = IntVar()

#Creando botones
lbl1 = Label(text='LUCES LATERALES:',font=('Verdana',6),foreground='#6d6e70').place(x=0,y=5)
txt1 = Entry(v,textvariable=luces_laterales,background='White',font=('Verdana',6),width=5).place(x=100,y=5)
lbl2 = Label(text='LUCES SUPERIORES:',font=('Verdana',6),foreground='#6d6e70').place(x=0,y=20)
txt2 = Entry(v,textvariable=luces_superiores,background='White',font=('Verdana',6),width=5).place(x=100,y=20)
btnAccion = Button(v,text='INICIAR',font=('Verdana',6),command=iniciar_programa,width=10).place(x=150,y=10)
btnAccion2 = Button(v,text='DETENER',font=('Verdana',6),command=detener_programa,width=10).place(x=220,y=10)
rdButton = Radiobutton(v,text='TIRA LEDS RGB DIGITAL',font=('Verdana',6),value=1,variable=modo).place(x=300,y=5)
rdButton2 = Radiobutton(v,text='TIRA LEDS RGB ANALOGA',font=('Verdana',6),value=2,variable=modo).place(x=300,y=20)

#Ejecutar ventana
v.after(500, capturando_pantalla)
v.mainloop()
