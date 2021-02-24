"""
AIR QUALITY MONITORING SYSTEM

@author: Paolo Santancini
"""


from modules import dht22
from modules import sds011
from modules import microelab
from modules import vk162
from modules import dag
from modules import io
import time, threading
import logging


DETECTIONS = 10 # sample size
CICLI = 2 # number of observations
SENSE_BOX = '601931c24f0ae0001b70092d' # Centrale di monitoraggio unique ID
SENSORID_1 = '601931c24f0ae0001b700931' # Temperature Sensor unique ID
SENSORID_2 = '601931c24f0ae0001b700930' # Humidity Sensor unique ID
SENSORID_3 = '601931c24f0ae0001b70092f' # PM10 Sensor unique ID
SENSORID_4 = '601931c24f0ae0001b70092e' # PM2.5 Sensor unique ID

# DAG SYSTEM PARAMS
iota_testnet = 'https://explorer.iota.org/devnet/transaction/'
api_url = 'https://nodes.devnet.iota.org:443'
address = 'WAGVEQ9JUZZWCZXLWVNTHBDX9G9KZTJP9VEERIIFHY9SIQKYBVAHIMLHXPQVE9IXFDDXNHQINXJDRPFDXNYVAPLZLZ'
buffer = '' # dag buffer writing

if __name__ == "__main__":

    format = "%(message)s"
    logging.basicConfig(format=format, filename='./data/senseBox.log', 
                        level=logging.INFO)
    
    objMicroe = microelab.Microelab('https://api.opensensemap.org/boxes/', 
                                    {'content-type': 'application/json'})
    objDht22 = dht22.Dht22(4, './data/dht22.log')
    objSds011 = sds011.Sds011('/dev/ttyUSB0', './data/sds011.log')
    objVk162 = vk162.Vk162("/dev/ttyACM0")
    objIota = dag.Dag(api_url, address)
    objIo = io.Io('./data/aqms_testset.csv')
    count = 0
    ts = time.time()
    logging.info("Partenza: %s", ts)
    while count < CICLI:        
        count = count + 1
        logging.info("Ciclo: %d",count)
        x = threading.Thread(target=objDht22.Acquiring(DETECTIONS))
        y = threading.Thread(target=objSds011.Acquiring(DETECTIONS))
        # acquiring sensor data
        x.start()
        y.start()
        x.join()
        y.join()
        # reading and elab sensor data
        (temperature, humidity, lines) = objDht22.getData()
        (pm10, pm2_5, lines) = objSds011.getData()
        (avgTemperature, avgHumidity) = objMicroe.getTH(temperature, humidity, lines) # temp and humidity math avarage
        (avgPm10, avgPm2_5) = objMicroe.getPP(pm10, pm2_5, lines) # pm10 and 2.5 math avarage
        (lon, lat) = objVk162.getPositionData() # read gps coordinates
        buffer = str(time.time())+";"+str(avgTemperature) + ";" + str(avgHumidity) + ";" + str(avgPm10) + ";" + str(avgPm2_5) + ";" + str(lon) + ";" + str(lat)
        # sending data to dag system and compose result message
        buffer = buffer + ";" + iota_testnet + str(objIota.doTransaction(buffer)) + "\n"
        # write down buffer values into csv file
        objIo.Open('a+')
        objIo.Write(buffer)
        objIo.Close()

        # sending values to opensensemap system
        req_num = 0
        flag = 0
        while True:
            status = objMicroe.updateOSM(SENSE_BOX,SENSORID_1,avgTemperature)            
            req_num = req_num + 1
            if ((status == 201) or (req_num > 2)):
                logging.info("POST Temperature %d",status)
                flag = 1
                break
            time.sleep(3)
        if (flag == 0):
            logging.info("POST Temperature %d",status)
            pass

        req_num = 0
        flag = 0
        while True:
            status = objMicroe.updateOSM(SENSE_BOX,SENSORID_2,avgHumidity)            
            req_num = req_num + 1
            if ((status == 201) or (req_num > 2)):
                logging.info("POST Humidity %d",status)
                flag = 1
                break
            time.sleep(3)
        if (flag == 0):
            logging.info("POST Humidity %d",status)
            pass    
        
        req_num = 0
        flag = 0
        while True:
            status = objMicroe.updateOSM(SENSE_BOX,SENSORID_3,avgPm10)            
            req_num = req_num + 1
            if ((status == 201) or (req_num > 2)):
                logging.info("POST PM10 %d",status)
                flag = 1
                break
            time.sleep(3)
        if (flag == 0):
            logging.info("POST PM10 %d",status)
            pass        
        
        req_num = 0
        flag = 0
        while True:
            status = objMicroe.updateOSM(SENSE_BOX,SENSORID_4,avgPm2_5)            
            req_num = req_num + 1
            if ((status == 201) or (req_num > 2)):
                logging.info("POST PM2.5 %d",status)
                flag = 1
                break
            time.sleep(3)
        if (flag == 0):
            logging.info("POST PM2.5 %d",status)
            pass

    ts = time.time()
    logging.info("Fine: %s", ts)
