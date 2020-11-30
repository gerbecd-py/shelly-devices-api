# shelly_api_get.py
Poll Shelly Relays and write Data to INFLUX Database

*Currently the script is only fetching the TEMPERATURE data from the Relays. Only the following models if Shelly are supported*:
- Shelly 1
- Shelly 1L
- Shelly 1PM
- Shelly 2.5

## Prerequisits
- Running INFLUX Database
- Running Grafana, connected to the INFLUX database

Search documentation for INFLUX and Grafana setup options on their respective websites.

## Required Python3 Modules
The following Python3 Modules need to be installed (either locally or system wide):
- json
- urllib.request
- datetime
- pytz
- influxdb
- argparse

You can you the command: python3 -m pip install <module> to install the modules

## Some configuration is required

To run this script, some configuration in the script will be needed. Please change the following, found in the script "Global Variables" and "InfluxDB Configuration":

- Global Variables
    - shellyUsername="<CHANGE>" -> Username to log into the Shelly Web Interface
    - shellyPassword="<CAHNGE>" -> Password to log into the Shelly Web Interface

- InfluxDB Configuration
    - databaseHost = "<CHANGE>" -> Hostname where your InfluxDB is Running
    - databasePort = "<CHANGE>" -> Port for communication, Typically 8086
    - databaseDatabase = "<CHANGE>" -> Database name to write to
    - databaseUsername = "<CHANGE>" -> Username for the Database
    - databasePassword = "<CHANGE>" -> Password for the Database

## Usage

###
    usage: shelly_api_get.py [-h] ip {temp} {1,1PM,1L,2.5}

    positional arguments:
      ip              Shelly IP Address
      {temp}          What data to poll (currently only relay temperature is available)
      {1,1PM,1L,2.5}  Currently Supported Shelly Devices

    optional arguments:
      -h, --help      show this help message and exit

## Example
###
    user@server:~ $ python3 shell_api_get.py 10.0.5.170 temp 1L

## Automate polling

If you wish to automate the polling, you could use crontab. Example crontab entry:

###
    * * * * * /usr/bin/python3 /home/user/python/test/shelly_api_get.py 10.0.5.170 temp 1L

This entry will run the script each minute and write the data to InfluxDB
