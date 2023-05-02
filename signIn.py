import serial
import datetime
import serial.tools.list_ports
import json




roomStatus = dict({"Students In":[]})

comlist = serial.tools.list_ports.comports() #finds barcode port and opens it
connected = []
for element in comlist:
    connected.append(element.device)
    if element.description == "barcode scanner":
        ser = serial.Serial(element.device)
    print("Barcode Scanner connected at:", ser.name)

        
def signingIn(student): #Keeps a list of all recorded scans
        #edit students scan status and time
        student["cur_visit"] = {str(datetime.datetime.now().time()):{
                "in":str(datetime.datetime.now().time()), 
                "out":"",
                "type": "office hours",
                "SRT":"name",
                "class":"class title",
                "Priority":0
              }}
        print("Student Signed In!")
        
def signingOut(student): #Keeps a list of all recorded scans
        #edit students scan status and history  
        visit = student["cur_visit"]
        visit["out"] = str(datetime.datetime.now().time())
        student["visits"][student["cur_visit"]]=visit
        student["cur_visit"]="None"
        json.dump(student, open(f'logs/{line}.json'),indent=4)
        print("Student Signed Out :(")

def getStudent(line):
    #find student with matching ID
    try:
        student = json.load(open(f'logs/{line}.json'))
    except:
        print("Student Not Found")
        student = {'id': line, 'name': 'tempName', 'Major': 'major', 'cur_visit': 'None', 'Visits': []}
        json.dump(student, open(f'logs/{line}.json'),indent=4)
    return student
            
while True: #checks for new input from barcode and updates dataframe
    line = ser.readline()
    line = line.decode('utf-8',errors='ignore').rstrip('/r/n')
    line = int(line)
    student = getStudent(line)
    ser.flush()
    print("\n\nName",student.name,"\n\n")
    if str(student['cur_visit']) == "None": #If student is signing in
        signingIn(student)
    else: #If student is signing out
        signingOut(student)
    #If time is pass hours
    #    for student in Students
