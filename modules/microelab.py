"""
MICRO ELABORATOR OBJECT CLASS

@author: Paolo Santancini
"""

import requests, json

class Microelab:
    
    def __init__(self, opensensemap_api_url, content):
        self.api_url = opensensemap_api_url
        self.content = content
    
    # getting temperature and humidity mathematical avarage
    def getTH(self, temperature, humidity, lines):
        avgTemperature = round((temperature / lines),2)
        avgHumidity = round((humidity / lines),2)
        return(avgTemperature, avgHumidity)        
    

    # getting PM10 and Pm2.5 mathematical avarage
    def getPP(self, pm10, pm2_5, lines):
        avgPm10 = round(pm10 / lines,2)
        avgPm2_5 = round(pm2_5 / lines,2)
        return(avgPm10, avgPm2_5)

    # Updating OpenSenseMap System
    # by senseBox and sensor
    def updateOSM(self,senseBox, sensorID, value):
        url = self.api_url+senseBox+'/'+ sensorID
        payload = {'value': value}
        try:
            r = requests.post(url, data=json.dumps(payload), headers=self.content)
        except:
            return(0)
        finally:
            return(r.status_code)
