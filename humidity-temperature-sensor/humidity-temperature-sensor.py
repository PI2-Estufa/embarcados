# Programa : Sensor de temperatura DHT11 com Raspberry Pi B+
# Autor : Eduardo_ssr

#
#   O programa funciona no modo BCM, logo o pino de dados do DHT22 deve 
#   ser conectado no GPIO.23, pino 16. Com um resistor de pull-up  entre 
#   o pino de dados e o VCC(3V3).
#
# 
#
# Carrega as bibliotecas
import Adafruit_DHT
import RPi.GPIO as GPIO
import time
 
# Define o tipo de sensor
#sensor = Adafruit_DHT.DHT11
sensor = Adafruit_DHT.DHT22
 
#GPIO.setmode(GPIO.BOARD)
 
# Define a GPIO conectada ao pino de dados do sensor
pino_sensor = 23
 
# Informacoes iniciais
print ("*** Lendo os valores de temperatura e umidade");
 
while(1):
   # Efetua a leitura do sensor
   umid, temp = Adafruit_DHT.read_retry(sensor, pino_sensor);
   # Caso leitura esteja ok, mostra os valores na tela
   if umid is not None and temp is not None:
     print ("Temperatura = {0:0.1f}  Umidade = {1:0.1f}\n").format(temp, umid);
     print ("Aguarda 5 segundos para efetuar nova leitura...\n");
     time.sleep(5)
   else:
     # Mensagem de erro de comunicacao com o sensor
     print("Falha ao ler dados do DHT22 !!!")
