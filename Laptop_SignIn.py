#!/usr/bin/env python3
import serial
import serial.tools.list_ports
import json
import time

SRT_occupancy = {
    "placeholder 0":{},
    "placeholder 1":{}, 
    "placeholder 2":{}
}

def serialSetup():
    ser = None
    comlist = serial.tools.list_ports.comports() #finds barcode port and opens it
    connected = []
    for element in comlist:
        connected.append(element.device)
        if element.description == "barcode scanner"or ("USB Serial Device" in element.description):
            ser = serial.Serial(element.device, timeout=0)
        print("Barcode Scanner connected at:", ser.name)
    if ser == None:
        print("No barcode scanner found, exiting")
        exit(0)
    return ser


def signingIn(student:dict, current_SRT:str): #Keeps a list of all recorded scans
        #edit students scan status and time
        student["cur_visit"] = {
                "in":time.strftime("%a, %d %b %Y %H:%M:%S"), 
                "out":"",
                "type": "office hours",
                "SRT":current_SRT,
                "class":"class title",
                "priority":0
              }
        json.dump(student, open(f'logs/{student["id"]}.json', 'w'),indent=4)
        #add student to SRT queue
        srtQueue(student, current_SRT, "in")
        print("Student Signed In!")
        return student
        
def signingOut(student:dict): #Keeps a list of all recorded scans
        #edit students scan status and history  
        visit = student["cur_visit"]
        srt = visit["SRT"]
        visit["out"] = time.strftime("%a, %d %b %Y %H:%M:%S")
        student["visits"][student["cur_visit"]["in"]]=visit
        student["cur_visit"]="None"
        json.dump(student, open(f'logs/{student["id"]}.json', 'w'),indent=4)
        # remove student from SRT queue
        srtQueue(student, srt, "out")
        print("Student Signed Out :(")
        return 

def getStudent(line:int):
    #find student with matching ID
    try:
        student = json.load(open(f'logs/{line}.json'))
    except:
        print("Student Not Found")
        student = {'id': line, 'name': 'tempName', 'major': 'major', 'cur_visit': 'None', 'visits': {}}
        with open(f'logs/{line}.json', 'w') as f:
            json.dump(student, f,indent=4)
    return student
            
def srtQueue(student:dict, srt:str, direction:str):
    #short form student info
    id = student["id"]
    # get SRT queue
    queue = SRT_occupancy[srt]
    if direction == "in":
        time_in = student["cur_visit"]["in"]
        class_in = student["cur_visit"]["class"]
        priority = student["cur_visit"]["priority"]
        student_short = {'id':student["id"], "name":student["name"],"major":student["major"], "time in":time_in, "class":class_in, "priority":priority}
        queue[id] = student_short
    elif direction == "out":
        if id in queue:
            del queue[id]
    SRT_occupancy[srt] = queue
    with open(f'logs/SRT_{srt.replace(" ", "_")}_queue.json', 'w') as f:
            json.dump(queue, f,indent=4)



def main():
    

    # find serial scanner
    ser = serialSetup()
    

    current_SRT = "placeholder 0"
    
    lasttime = time.time()
    last_id = None
    
    try:
        while True: #checks for new input from barcode and updates dataframe
            line = ser.readline()
            if len(line) > 3:
                line = line.decode('utf-8',errors='ignore').rstrip('/r/n')
                try:
                    line = int(line)
                    print(f'\nScanner reads: \n{line}')
                    if last_id != line:
                        student = getStudent(line)
                        ser.flush()
                        print(f'Name: {student["name"]}')
                        if str(student['cur_visit']) == "None": #If student is signing in
                            signingIn(student, current_SRT)
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
        print("\n Shutting down scanner")
        ser.close()
        print("Exiting")


main()