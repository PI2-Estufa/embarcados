#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from time import sleep
import numpy as np
import threading
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)

pinMotor1 = 40 #gpio 20
pinMotor2 = 32 #gpio 26
pinReed1  = 36 #gpio 16
pinReed2  = 35 #gpio 19
pinPorta  = 33 #gpio 13

GPIO.setup(pinMotor1, GPIO.OUT)
GPIO.setup(pinMotor2, GPIO.OUT)
GPIO.setup(pinReed1, GPIO.IN)
GPIO.setup(pinReed2, GPIO.IN)
GPIO.setup(pinPorta, GPIO.IN)

GPIO.output(pinMotor1, GPIO.LOW)
GPIO.output(pinMotor2, GPIO.LOW)

estado = 'i' 

motor1 = 0
motor2 = 0

#t = 2

reedPorta = 1
c = 0
reed1 = 0
reed2 = 1

def start(porta,comando,reed1,reed2):
    
    global estado
    global motor1
    global motor2
    
    sleep(0.001)
    
    motor1 = 0
    motor2 = 0
    estado = 0
    
def eFechado(porta,comando,reed1,reed2):
    
    global estado
    global motor1
    global motor2
    
    motor1 = 0
    motor2 = 0
    
    print ("Gaveta fechada. ")
    #sleep(t)
    if ((porta == 1) and (comando == '0' or comando =='1')) or (comando == '0'):
        estado = 0
    elif (comando == '1' and porta == 0):
        estado = 1


def eAbrindo(porta,comando, reed1, reed2):
    
    global estado
    global motor1 
    global motor2
    print("Abrindo gaveta")
    if reed2 == 0: 
        motor1 = 0
        motor2 = 1
        estado = 1
    else:
        motor1 = 0
        motor2 = 0
        estado = 2
	#sleep(t)
    
    
def eAberto(porta, comando, reed1, reed2):
    
    global estado 
    global motor1
    global motor2

    print("Gaveta aberta")
    motor1 = 0 
    motor2 = 0
    if(comando == '1'):
        estado = 2
    else:
        estado = 3 

def eFechando(porta, comando, reed1, reed2):
    
    global estado
    global motor1
    global motor2
    print ("Fechando Gaveta")  
    if reed1 == 0: 	
        motor1 = 1
        motor2 = 0
        estado = 3
    else:
        motor1 = 0
        motor2 = 0
        estado = 0
    
def maquinaEstados(porta, comando, reed1, reed2 ):
    global estado 
    
    if estado == 'i':
        start(porta, comando, reed1, reed2)
    elif estado == 0:
        eFechado(porta, comando, reed1, reed2)
    elif estado == 1:
        eAbrindo(porta, comando, reed1, reed2)
    elif estado == 2:
        eAberto(porta, comando, reed1, reed2)
    elif estado == 3:
        eFechando(porta, comando, reed1, reed2)
    else:
        start(porta, comando, reed1, reed2) 

def estadoMotor(m1,m2):	
    if m1 == 1:
        GPIO.output(pinMotor1, GPIO.HIGH)
    else:
        GPIO.output(pinMotor1, GPIO.LOW)
    
    if m2 == 1:
        GPIO.output(pinMotor2, GPIO.HIGH)
    else:
        GPIO.output(pinMotor2, GPIO.LOW)

def controleGaveta():
    global c
    global reedPorta
    global reed1
    global reed2
    global motor1
    global motor2
   # interrupt = 0
    while(True):
        maquinaEstados(reedPorta, c, reed1, reed2)
        sleep(0.1)
        estadoMotor(motor1,motor2)
       # if p == '1' and estado == 2:
       #     interrupt =1

gaveta = threading.Thread(target=controleGaveta)  
gaveta.start()

while(True):
    if GPIO.input(pinPorta)	== GPIO.HIGH:
        reedPorta = 1 #porta fechada
        print("Porta fechada")
    else:
        reedPorta = 0 #porta aberta
        print("Porta aberta")
    
    if GPIO.input(pinReed1) == GPIO.HIGH:
        reed1 = 1
        print("Reed traseiro ativado")
    else:
        reed1 = 0
        print("Reed traseiro desativado")
    
    if GPIO.input(pinReed2) == GPIO.HIGH:
        reed2 = 1
        print("Reed dianteiro ativado")
    else:
        reed2 = 0
        print("Reed dianteiro desativado")

    c = input("Quer a gaveta aberta ou fechada(0 = fechada e 1 = aberta): ")	
