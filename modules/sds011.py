"""
SDS011 SENSOR OBJECT CLASS
Created on Thu Feb 11 18:51:23 2021

@author: Paolo Santancini
"""

import serial

class Sds011:

    SDS011_LOG = './data/sds011.log'
    SER = serial.Serial('/dev/ttyUSB0')
    
    def __init__(self):
        pass
    
    def Acquiring(self, DETECTIONS):
        count = 0
        f = open(Sds011.SDS011_LOG, 'w')
        while count < DETECTIONS:
            data = []
            for index in range(0,10):
                datum = Sds011.SER.read()
                data.append(datum)
            pmtwofive = int.from_bytes(b''.join(data[2:4]), byteorder='little') / 10
            pmten = int.from_bytes(b''.join(data[4:6]), byteorder='little') / 10
            f.write(f'{pmtwofive};{pmten}\n')
            count = count + 1
        f.close()