#!/usr/bin/env python
 
import os
import xively
import subprocess
import time
import datetime
import requests
import serial
 
# extract feed_id and api_key from environment variables
FEED_ID = "803439804"
API_KEY = "4OysxNVaHiB1cwavaoKMXywwXdw1KYZaMODHdA8ZcrS9nxO0"
DEBUG = os.environ["DEBUG"] or false

# read serial
ser = serial.Serial("/dev/ttyACM0")
read = ser.read(19)
# initialize api client
api = xively.XivelyAPIClient(API_KEY)
 
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

def get_num(read):
	return float(''.join(ele for ele in read if ele.isdigit() or ele == '.')) 
# main program entry point - runs continuously updating our datastream with the
# current 1 minute load average
def run():
  print "Starting Xively tutorial script"
 
  feed = api.feeds.get(FEED_ID)
 
  datastream = get_datastream(feed)
  datastream.max_value = None
  datastream.min_value = None
 
  while True:
    load_avg = get_num(read)
 
    if DEBUG:
      print "Updating Xively feed with value: %s" % load_avg
 
    datastream.current_value = load_avg
    datastream.at = datetime.datetime.utcnow()
    try:
      datastream.update()
    except requests.HTTPError as e:
      print "HTTPError({0}): {1}".format(e.errno, e.strerror)
 
    time.sleep(1)
 
run()
