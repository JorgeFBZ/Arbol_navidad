try:
  import usocket as socket
except:
  import socket

from machine import Pin, PWM
from random import randint
import network

import esp
esp.osdebug(None)

import gc
gc.collect()

ssid = 'MiFibra-8C12-24G'
password = 'uWbKbQs4'

station = network.WLAN(network.STA_IF)

station.active(True)
station.connect(ssid, password)

while station.isconnected() == False:
  pass

print('Connection successful')
print(station.ifconfig())

freq= 5000
colores = [12,14,27]
ciclo = 10

verde = 14
azul = 27
rojo =12
led_verde = Pin(verde, Pin.OUT)
led_azul = Pin(azul, Pin.OUT)
led_rojo = Pin(rojo, Pin.OUT)