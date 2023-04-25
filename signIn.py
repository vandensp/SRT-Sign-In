import serial
import serial.tools.list_ports

scanHistory = dict({"Barcodes":[]})
signedIn = []

comlist = serial.tools.list_ports.comports() #finds barcode port and opens it
connected = []
for element in comlist:
    connected.append(element.device)
    if element.description == "barcode scanner":
        ser = serial.Serial(element.device)
    print("Barcode Scanner connected at:", ser.name)

def storeScan(line):
    scanHistory["Barcodes"].append(line)
    print("Scan Stored")
    print(scanHistory)

while True: #checks for new input from barcode and updates dataframe
    line = ser.readline()
    line = line.decode('utf-8',errors='ignore').rstrip('/r/n')
    line = int(line)
    storeScan(line)
