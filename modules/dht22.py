"""
DHT22 SENSOR OBJECT CLASS
Created on Thu Feb 11 18:51:23 2021

@author: Paolo Santancini
"""

import Adafruit_DHT

class Dht22:
    
    DHT22_LOG = './data/dht22.log'
    DHT_SENSOR = Adafruit_DHT.DHT22
    
    def __init__(self, dht_pin):
        self.dht_pin = dht_pin
        
    def Acquiring(self, detections):
        count = 0
        f = open(Dht22.DHT22_LOG, 'w')
        while count < detections:
            humidity, temperature = Adafruit_DHT.read_retry(Dht22.DHT_SENSOR, self.dht_pin)
            if humidity is not None and temperature is not None:
                f.write(f'{temperature};{humidity}\n')
                count=count+1
        f.close()
