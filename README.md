# AQSM
AIR QUALITY SYSTEM MONITOR

This system provide an efficient acquiring of pm10, pm2.5, humidity and temperature values by sensors sds011, dht22 into raspberry pi os.
The data collection is made consistent through the use of a blockchain technology (IOTA's devnet https://explorer.iota.org/devnet/) and processed by some data mining algorithms.

## Install
This project is written in python3 and requires sds011 (http://www.inovafitness.com/en/a/chanpinzhongxin/95.html), dht22 (https://www.adafruit.com/product/385) sensors and a gps receiver plugged to a raspberry pi. In this case it uses pi 3 b+ with Linux raspberrypi 5.4.83-v7+ #1379 SMP Mon Dec 14 13:08:57 GMT 2020 armv7l GNU/Linux.

Follow these steps to run it:

1. clone the project
2. cd aqsm
2. install Adafruit_DHT by: sudo pip3 install Adafruit_DHT
3. install python iota modules: sudo pip3 install pyota
4. run: python3 main.py

## Data-Mining
"datamining_elab.py" is a Google Colab sperimental page. It gets a dataset (.csv) and applies k-means algorithm.
