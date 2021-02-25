"""
VK-162 GPS RECEIVER OBJECT

@author: Paolo Santancini
"""

import serial

class Vk162:
    
    def __init__(self, serial):
        self.serial = serial

# In the NMEA message, the position gets transmitted as:
# DDMM.MMMMM, where DD denotes the degrees and MM.MMMMM denotes
# the minutes. However, I want to convert this format to the following:
# DD.MMMM. This method converts a transmitted string to the desired format
    def formatDegreesMinutes(self, coordinates, digits):
        parts = coordinates.split(".")
        if (len(parts) != 2):
            return coordinates
        if (digits > 3 or digits < 2):
            return coordinates
        left = parts[0]
        right = parts[1]
        degrees = str(left[:digits])
        minutes = str(right[:3])

        return degrees + "." + minutes

# This method reads the data from the serial port, the GPS dongle is attached to,
# and then parses the NMEA messages it transmits.
# gps is the serial port, that's used to communicate with the GPS adapter
    def getPositionData(self,lon,lat):
        gps = serial.Serial(self.serial, 9600)
        data = str(gps.readline())
        gps.close()
        if '$GPRMC' in data:
        # GPRMC = Recommended minimum specific GPS/Transit data
        # Reading the GPS fix data is an alternative approach that also works
            parts = data.split(",")
            if parts[2] == 'V':
                # V = Warning, most likely, there are no satellites in view...
                return (lon,lat)
            else:
            # Get the position data that was transmitted with the GPRMC message
            # In this example, I'm only interested in the longitude and latitude
            # for other values, that can be read, refer to: http://aprs.gids.nl/nmea/#rmc
                #longitude = Vk162.formatDegreesMinutes(parts[5], 3)
                longitude = parts[5]
                #latitude = Vk162.formatDegreesMinutes(parts[3], 2)
                latitude = parts[3]
                return(str(longitude),str(latitude))
        else:
            return('E','E')
