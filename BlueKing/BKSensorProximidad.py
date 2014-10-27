# vim: set fileencoding=UTF-8 :

__author__ = 'fredericpena'

import time
import RPi.GPIO as GPIO
from PyQt4 import QtGui, QtCore

class BKSensorProximidad(QtCore.QThread):

    def __init__(self, sensor_id, gpio_i, gpio_o):
        QtCore.QThread.__init__(self)
        self.detenido = 0
        self.id_sensor = sensor_id
        self.gpio_in = gpio_i
        self.gpio_out = gpio_o
        self.fix_factor = 0.1

        #Configurar puertos
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)

        GPIO.setup(self.gpio_in, GPIO.IN)
        GPIO.setup(self.gpio_out, GPIO.OUT)
        GPIO.output(self.gpio_out, GPIO.LOW)

    def __del__(self):
        self.wait()

    def stop(self):
        self.detenido = 1

    def run(self):
        print("Sensor " + `self.id_sensor` + " iniciado... (in: " + `self.gpio_in` + " out: " + `self.gpio_out` + ")...")
        while self.detenido == 0:
            GPIO.output(self.gpio_out, True)
            time.sleep(0.00001)
            GPIO.output(self.gpio_out, False)

            senal_on = senal_off = 0

            while GPIO.input(self.gpio_in) == 0:
                senal_off = time.time()

            while GPIO.input(self.gpio_in) == 1 and (senal_on - senal_off) < 0.38:
                senal_on = time.time()

            tiempo = senal_on - senal_off

            if tiempo > 0.038:
                print("Fuera de Rango o mal alineado...")
                continue

            print("Tiempo sensor: " + `tiempo` + " us")

            distancia = round(((tiempo * 340) / 2), 1)

            if distancia > 10000:
                continue

            #Señalar la distancia
            print("Distancia sensor " + `self.id_sensor` + ": " + `distancia` + " m")
            self.emit(QtCore.SIGNAL("distancia_sensor"), distancia)

            time.sleep(1)

        self.terminate()

    def terminate(self):
        GPIO.cleanup()