# Air Quality Monitoring System
#
# Paolo Santancini - rel. 04.02.2021


import Adafruit_DHT
import serial, time, csv, threading
import requests, json
import logging


RILEVAZIONI = 60
CICLI = 1800
SENSE_BOX = '601931c24f0ae0001b70092d' # Centrale di monitoraggio
SENSORID_1 = '601931c24f0ae0001b700931' # Sonda Temperatura
SENSORID_2 = '601931c24f0ae0001b700930' # Sonda Umidità
SENSORID_3 = '601931c24f0ae0001b70092f' # Sonda PM10
SENSORID_4 = '601931c24f0ae0001b70092e' # Sonda PM2.5
DHT22_LOG = './data/dht22.log'
SDS011_LOG = './data/sds011.log'

def dht22(param):
	DHT_SENSOR = Adafruit_DHT.DHT22
	DHT_PIN = 4
	count = 0

	f = open(DHT22_LOG, 'w')
	while count < RILEVAZIONI:
		humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
		if humidity is not None and temperature is not None:
#			print("Temp={0:0.1f}*C    Humidity={1:0.1f}%".format(temperature, humidity))
			f.write(f'{temperature};{humidity}\n')
		count=count+1
	f.close()



def sds011(param):
	ser = serial.Serial('/dev/ttyUSB0')
	count = 0

	f = open(SDS011_LOG, 'w')
	while count < RILEVAZIONI:
		data = []
		for index in range(0,10):
			datum = ser.read()
			data.append(datum)
		pmtwofive = int.from_bytes(b''.join(data[2:4]), byteorder='little') / 10
		pmten = int.from_bytes(b''.join(data[4:6]), byteorder='little') / 10
		f.write(f'{pmtwofive};{pmten}\n')
		count = count + 1
	f.close()

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
    
    
    count = 0
    ts = time.time()
    logging.info("Partenza: %s", ts)
    while count < CICLI:        
        count = count + 1
        logging.info("Ciclo: %d",count)
        x = threading.Thread(target=dht22, args=('',))
        y = threading.Thread(target=sds011, args=('',))
        # acquisizione dei valori
        x.start()
        y.start()
        x.join()
        y.join()
        z = threading.Thread(target=elab, args=('',))
        z.start()
        z.join()

    ts = time.time()
    logging.info("Fine: %s", ts)
