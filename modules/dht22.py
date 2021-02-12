"""
DHT22 SENSOR OBJECT CLASS

@author: Paolo Santancini
"""

import Adafruit_DHT
from modules import io

class Dht22:
    
    DHT_SENSOR = Adafruit_DHT.DHT22
    
    def __init__(self, dht_pin, filelog):
        self.dht_pin = dht_pin
        self.filelog = filelog
        
    def Acquiring(self, detections):
        output = io.Io(self.filelog)
        output.Open()
        count = 0
        while count < detections:
            humidity, temperature = Adafruit_DHT.read_retry(Dht22.DHT_SENSOR, self.dht_pin)
            string = f'{temperature};{humidity}\n'
            output.Write(string) # write in buffer
            count=count+1
        output.Close()
    
    def getData(self):
        objIo = io.Io(self.filelog)
        return (objIo.getCsvData())
        
