"""
AIR QUALITY MONITORING SYSTEM
Created on Thu Feb 11 18:51:23 2021

@author: Paolo Santancini
"""


from modules import dht22
from modules import sds011
import time, csv, threading
import requests, json
import logging


DETECTIONS = 3 # sample size
CICLI = 1
SENSE_BOX = '601931c24f0ae0001b70092d' # Centrale di monitoraggio
SENSORID_1 = '601931c24f0ae0001b700931' # Sonda Temperatura
SENSORID_2 = '601931c24f0ae0001b700930' # Sonda Umidità
SENSORID_3 = '601931c24f0ae0001b70092f' # Sonda PM10
SENSORID_4 = '601931c24f0ae0001b70092e' # Sonda PM2.5
SDS011_LOG = './data/sds011.log'



def elab(param):
    
    hd = {'content-type': 'application/json'}
    
    # reading values from log files
    temperature = 0.0
    humidity = 0.0
    pm10 = 0.0
    pm2_5 = 0.0
    lines = 0
    with open(DHT22_LOG) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')
        for row in csv_reader:
            temperature += float(row[0])
            humidity += float(row[1])
            lines = lines + 1
    
        # media aritmetica
        temperature = round((temperature / lines),2)
        humidity = round((humidity / lines),2)
        #print(f'T={temperature} H={humidity} {lines}')

    lines = 0
    with open(SDS011_LOG) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')
        for row in csv_reader:
            pm10 += float(row[0])
            pm2_5 += float(row[1])
            lines = lines + 1
        
        # media aritmetica
        pm10 = round(pm10 / lines,2)
        pm2_5 = round(pm2_5 / lines,2)
        #print(f'PM10={pm10} PM2.5={pm2_5} {lines}')
	
	# Aggiornamento openSenseMap
    url = 'https://api.opensensemap.org/boxes/'+SENSE_BOX+'/'+SENSORID_1
    payload = {'value': temperature}
    req_num = 0
    flag = 0
    while True:
        r = requests.post(url, data=json.dumps(payload), headers=hd)
        req_num = req_num + 1
        if ((r.status_code == 201) or (req_num > 2)):
            logging.info("POST Temperature %d",r.status_code)
            flag = 1
            break
        time.sleep(3)
    if (flag == 0):
        logging.info("POST Temperature %d",r.status_code)

    url = 'https://api.opensensemap.org/boxes/'+SENSE_BOX+'/'+SENSORID_2
    payload = {'value': humidity}
    req_num = 0    
    flag = 0
    while True:
        r = requests.post(url, data=json.dumps(payload), headers=hd)
        req_num = req_num + 1
        if ((r.status_code == 201) or (req_num > 2)):
            logging.info("POST Humidity %d",r.status_code)
            flag = 1
            break
        time.sleep(3)
    if (flag == 0):
        logging.info("POST Humidity %d",r.status_code)
    
    url = 'https://api.opensensemap.org/boxes/'+SENSE_BOX+'/'+SENSORID_3
    payload = {'value': pm10}
    req_num = 0
    flag = 0
    while True:
        r = requests.post(url, data=json.dumps(payload), headers=hd)
        req_num = req_num + 1
        if ((r.status_code == 201) or (req_num > 2)):
            logging.info("POST PM10 %d",r.status_code)
            flag = 1
            break
        time.sleep(3)
    if (flag == 0):
        logging.info("POST PM10 %d",r.status_code)
    
    url = 'https://api.opensensemap.org/boxes/'+SENSE_BOX+'/'+SENSORID_4
    payload = {'value': pm2_5}
    req_num = 0
    flag = 0
    while True:
        r = requests.post(url, data=json.dumps(payload), headers=hd)
        req_num = req_num + 1
        if ((r.status_code == 201) or (req_num > 2)):
            logging.info("POST PM2.5 %d",r.status_code)
            flag = 1
            break
        time.sleep(3)
    if (flag == 0):
        logging.info("POST PM2.5 %d",r.status_code)
    
    # Aggiornamento DB
    

if __name__ == "__main__":

    format = "%(message)s"
    logging.basicConfig(format=format, filename='./data/senseBox.log', level=logging.INFO)
    
    objDht22 = dht22.Dht22(4)
    objSds011 = sds011.Sds011()
    count = 0
    ts = time.time()
    logging.info("Partenza: %s", ts)
    while count < CICLI:        
        count = count + 1
        logging.info("Ciclo: %d",count)
        x = threading.Thread(target=objDht22.Acquiring(DETECTIONS))
        y = threading.Thread(target=objSds011.Acquiring(DETECTIONS))
        # acquisizione dei valori
        x.start()
        y.start()
        x.join()
        y.join()
        #z = threading.Thread(target=elab, args=('',))
        #z.start()
        #z.join()

    ts = time.time()
    logging.info("Fine: %s", ts)
