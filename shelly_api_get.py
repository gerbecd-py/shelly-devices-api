from json import loads
import urllib.request
from datetime import datetime
from pytz import timezone
from influxdb import InfluxDBClient
import argparse

"""
Query Shelly Devices and retrive status information.

"""

___version___ = 0.1

config = argparse.ArgumentParser()
config.add_argument("ip", help="Shelly IP Address", type=str)
config.add_argument("data", help="What data to poll (currently only relay temperature is available)", type=str, choices=["temp"])
config.add_argument("shelly", help="Currently Supported Shelly Devices", type=str, choices=["1","1PM","1L","2.5"])
configValues = config.parse_args()

# Global Variables
shellyUsername="CHANGE"
shellyPassword="CHANGE"
shellyIP = configValues.ip
dataType = configValues.data
shellyType = configValues.shelly

# InfluxDB Configuration
databaseHost = "CHANGE"
databasePort = "CHANGE"
databaseDatabase = "CHANGE"
databaseUsername = "CHANGE"
databasePassword = "CHANGE"

def connectToDatabase():

    """
    Function to initiate Database Connection
    """

    # Database Connection: (influxdb)
    influxClient = InfluxDBClient(
                                host=databaseHost,
                                port=databasePort,
                                database=databaseDatabase,
                                username=databaseUsername,
                                password=databasePassword,
                                timeout=5
                                )

    return influxClient

def getAPIResult():

    """Function to get the REST API result needed from 'url'"""

    url = "http://{}/status".format(shellyIP)

    # Handle Shelly Basic Authentication
    password_mgr = urllib.request.HTTPPasswordMgrWithDefaultRealm()
    password_mgr.add_password(None, url, shellyUsername, shellyPassword)
    handler = urllib.request.HTTPBasicAuthHandler(password_mgr)
    opener = urllib.request.build_opener(handler)
    urllib.request.install_opener(opener)

    # Get the data requested
    restApiUrlOpen = urllib.request.urlopen(url, timeout=5).read()
    result = loads(restApiUrlOpen)
    return result

contents = getAPIResult()

if dataType == "temp":
    dataBody = {}
    dataBody['time'] = datetime.now(timezone('Europe/Vienna'))

    dataBody['measurement'] = "Shelly %s, %s" % (shellyType, shellyIP)
    dataBody['tags'] = { 'sensor': 'temperature' }
    dataBody['fields'] = { 'value': contents['temperature'] }
    connectToDatabase().write_points([dataBody])
