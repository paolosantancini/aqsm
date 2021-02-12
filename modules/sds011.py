"""
SDS011 SENSOR OBJECT CLASS

@author: Paolo Santancini
"""

import serial
from modules import io

class Sds011:
    
    def __init__(self, device, filelog):
        self.device = device
        self.filelog = filelog
    
    def Acquiring(self, DETECTIONS):
        SER = serial.Serial(self.device)
        output = io.Io(self.filelog)
        output.Open()
        count = 0
        while count < DETECTIONS:
            data = []
            for index in range(0,10):
                datum = SER.read()
                data.append(datum)
            # read 2:4 bytes for PM2.5 value
            pmtwofive = int.from_bytes(b''.join(data[2:4]), 
                                       byteorder='little') / 10
            # read 4:6 bytes for PM10 value
            pmten = int.from_bytes(b''.join(data[4:6]), 
                                   byteorder='little') / 10
            string = f'{pmtwofive};{pmten}\n'
            output.Write(string) # write in buffer
            count = count + 1
        output.Close()
    
    def getData(self):
        objIo = io.Io(self.filelog)
        return (objIo.getCsvData())