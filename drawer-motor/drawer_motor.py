#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
from time import sleep
from kombu import Connection, Queue, Exchange
from kombu.mixins import ConsumerMixin
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

drawer_state = ''

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
    global drawer_state
    
    motor1 = 0
    motor2 = 0
    
    drawer_state = "Gaveta fechada. "


    #sleep(t)
    if ((porta == 1) and (comando == '0' or comando =='1')) or (comando == '0'):
        estado = 0
    elif (comando == '1' and porta == 0):
        estado = 1


def eAbrindo(porta,comando, reed1, reed2):
    
    global estado
    global motor1 
    global motor2
    global drawer_state
    global reedPorta

    if reedPorta == 1:
        return

    drawer_state = "Abrindo gaveta"

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
    global drawer_state

    drawer_state = "Gaveta aberta"

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
    global drawer_state

    drawer_state = "Fechando Gaveta"

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

def ameixa(command):
    global reedPorta
    global reed1
    global reed2
    global c
    global drawer_state

    print(drawer_state)
    if drawer_state == "Gaveta aberta" or drawer_state == "Abrindo gaveta":
        signal = '0'
    else: 
        signal = '1'

    for i in list(range(10)):
        sleep(.5)
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

        c = signal 
        print(drawer_state)


class DrawerMaster(ConsumerMixin):

    def __init__(self, connection):
        print('worker starting')
        self.connection = connection

    def get_consumers(self, Consumer, channel):
        return [Consumer(queues=queues, callbacks=[self.process])]

    def process(self, body, message):
        command = body['command']
        print(command)
        ameixa(command)
        message.ack()


if __name__ == '__main__':
    exchange = Exchange('rdrawer', type='direct')
    queues = [Queue('rdrawer', exchange, routing_key='rdrawer')]

    with Connection(os.environ.get('RABBIT_URL')) as conn:
        try:
            worker = DrawerMaster(conn)
            worker.run()
        except KeyboardInterrupt:
            print('buh bye')

