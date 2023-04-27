#!/usr/bin/python3
import serial
import serial.tools.list_ports
import time

scanHistory = dict({"Barcodes":[]})
signedIn = []

comlist = serial.tools.list_ports.comports() #finds barcode port and opens it
connected = []
ser = None
for element in comlist:
    connected.append(element.device)
    print(element.description)
    if ("barcode scanner" in element.description) or ("USB Serial Device" in element.description):
        ser = serial.Serial(element.device,timeout=5)
        print("Barcode Scanner connected at:", ser.name)

if ser == None:
    exit(0)

def storeScan(line):
    scanHistory["Barcodes"].append(line)
    print("Scan Stored")
    print(scanHistory)

lasttime = time.time()
last_id = None
try:
    while True: #checks for new input from barcode and updates dataframe
        line = ser.readline()
        if len(line) > 3:
            line = line.decode('utf-8',errors='ignore').rstrip('/r/n')
            try:
                line = int(line)
                if last_id != line:
                    storeScan(line)
                    last_id = line
                else: 
                    print("double scanned")
            except ValueError:
                print("not an int value, was:", line)
        if time.time()-lasttime > 5: 
            last_id = None
            lasttime = time.time()
except KeyboardInterrupt:
    ser.close()
    exit(0)
        
        
