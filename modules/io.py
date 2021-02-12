"""
INPUT/OUTPUT OPERATIONAL OBJECT CLASS

@author: Paolo Santancini
"""

import csv

class Io:
    
    f = ''
    
    def __init__(self, filelog):
        self.filelog = filelog
        
    def Open(self):
        Io.f = open(self.filelog, 'w')
        
    def Close(self):
        Io.f.close()
        
    def Write(self, string):
        Io.f.write(string)

    def getCsvData(self):
        lines = 0
        c1 = c2 = 0
        with open(self.filelog) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=';')
            for row in csv_reader:
                c1 += float(row[0])
                c2 += float(row[1])
                lines = lines + 1
        return(c1,c2,lines)