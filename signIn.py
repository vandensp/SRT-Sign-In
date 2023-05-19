#!/usr/bin/env python3
import serial
import serial.tools.list_ports
import json
import time



roomStatus = dict({"Students In":[]})

comlist = serial.tools.list_ports.comports() #finds barcode port and opens it
connected = []
for element in comlist:
    connected.append(element.device)
    if element.description == "barcode scanner"or ("USB Serial Device" in element.description):
        ser = serial.Serial(element.device, timeout=5)
    print("Barcode Scanner connected at:", ser.name)

if ser == None:
    exit(0)

        
def signingIn(student): #Keeps a list of all recorded scans
        #edit students scan status and time
        student["cur_visit"] = {
                "in":time.strftime("%a, %d %b %Y %H:%M:%S"), 
                "out":"",
                "type": "office hours",
                "SRT":"name",
                "class":"class title",
                "Priority":0
              }
        json.dump(student, open(f'logs/{student["id"]}.json', 'w'),indent=4)
        print("Student Signed In!")
        return student
        
def signingOut(student): #Keeps a list of all recorded scans
        #edit students scan status and history  
        visit = student["cur_visit"]
        visit["out"] = time.strftime("%a, %d %b %Y %H:%M:%S")
        student["visits"][student["cur_visit"]["in"]]=visit
        student["cur_visit"]="None"
        json.dump(student, open(f'logs/{student["id"]}.json', 'w'),indent=4)
        print("Student Signed Out :(")

def getStudent(line):
    #find student with matching ID
    try:
        student = json.load(open(f'logs/{line}.json'))
    except:
        print("Student Not Found")
        student = {'id': line, 'name': 'tempName', 'major': 'major', 'cur_visit': 'None', 'visits': {}}
        with open(f'logs/{line}.json', 'w') as f:
            json.dump(student, f,indent=4)
    return student
            

lasttime = time.time()
last_id = None
try:
    while True: #checks for new input from barcode and updates dataframe
        line = ser.readline()
        if len(line) > 3:
            line = line.decode('utf-8',errors='ignore').rstrip('/r/n')
            try:
                line = int(line)
                print(line)
                if last_id != line:
                    student = getStudent(line)
                    ser.flush()
                    print("\n\nName",student["name"],"\n\n")
                    if str(student['cur_visit']) == "None": #If student is signing in
                        signingIn(student)
                    else: #If student is signing out
                        signingOut(student)
                    #If time is pass hours
                    #    for student in Students
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