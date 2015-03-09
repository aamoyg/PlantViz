#!/usr/bin/env python
 
import os
import xively
import subprocess
import time
import datetime
import requests
import serial
 
# extract feed_id and api_key from environment variables
FEED_ID = "803439804" #temp
FEED_ID2 = "1208007568" #humidity
FEED_ID3 = "1812851084" #light
API_KEY = "4OysxNVaHiB1cwavaoKMXywwXdw1KYZaMODHdA8ZcrS9nxO0"
API_KEY2 = "7lIgzoL0kqVKTKnoALUmMPPm6asUqjDsrXltHpQrMAW6KrdX"
API_KEY3 = "qvmVLgPcR3YnjVXn0IZ7EZvVpPebuj7ofI5NpVEiBskL5OqH"
DEBUG = os.environ["DEBUG"] or false

# read serial
ser = serial.Serial("/dev/ttyACM0")
read = ser.read(5)
read2 = ser.read(5)
read3 = ser.read(5)
# initialize api client
api = xively.XivelyAPIClient(API_KEY)
api2 = xively.XivelyAPIClient(API_KEY2)
api3 = xively.XivelyAPIClient(API_KEY3)
 
# function to read 1 minute load average from system uptime command
def read_loadavg():
  if DEBUG:
    print "Reading load average"
  return subprocess.check_output(["awk '{print $1}' /proc/loadavg"], shell=True)
 
# function to return a datastream object. This either creates a new datastream,
# or returns an existing one
def get_datastream(feed):
  try:
    datastream = feed.datastreams.get("temperature")
    if DEBUG:
      print "Found existing datastream"
    return datastream
  except:
    if DEBUG:
      print "Creating new datastream"
    datastream = feed.datastreams.create("temperature", tags="temp_01")
    return datastream

def get_datastream2(feed):
  try:
    datastream = feed.datastreams.get("humidity")
    if DEBUG:
      print "Found existing datastream"
    return datastream
  except:
    if DEBUG:
      print "Creating new datastream"
    datastream = feed.datastreams.create("humidity", tags="humidity_01")
    return datastream

def get_datastream3(feed):
  try:
    datastream = feed.datastreams.get("light")
    if DEBUG:
      print "Found existing datastream"
    return datastream
  except:
    if DEBUG:
      print "Creating new datastream"
    datastream = feed.datastreams.create("light", tags="light_01")
    return datastream

def get_num(read):
	return float(''.join(ele for ele in read if ele.isdigit() or ele == '.')) 
# main program entry point - runs continuously updating our datastream with the
# current 1 minute load average
def run():
  print "Starting Xively tutorial script"
 
  feed = api.feeds.get(FEED_ID)
  feed2 = api2.feeds.get(FEED_ID2)
  feed2 = api3.feeds.get(FEED_ID3)
 
  datastream = get_datastream(feed)
  datastream2 = get_datastream2(feed2)
  datastream3 = get_datastream3(feed3)
  
  datastream.max_value = None
  datastream.min_value = None
 
  while True:
    load_avg = get_num(read)
    load_avg2 = get_num(read2)
    load_avg3 = get_num(read3)
 
    if DEBUG:
      print "Updating Xively feed with value: %s" % load_avg % load_avg2 % load_avg3
 
    datastream.current_value = load_avg
    datastream.at = datetime.datetime.utcnow()

    datastream2.current_value = load_avg2
    datastream2.at = datetime.datetime.utcnow()

    datastream3.current_value = load_avg3
    datastream3.at = datetime.datetime.utcnow()
    
    try:
      datastream.update()
      datastream2.update()
      datastream3.update()
    except requests.HTTPError as e:
      print "HTTPError({0}): {1}".format(e.errno, e.strerror)
 
    time.sleep(1)
 
run()
