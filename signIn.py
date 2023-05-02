import serial
import datetime
import serial.tools.list_ports
import pandas as pd

studentRecord = pd.read_csv("studentRecords.csv")
visitHistory = dict({"studentID":[], "name":[],"major":[],"Sign-in Time":[],"Sign-out Time":[]})
roomStatus = dict({"Students In":[]})
historyDF = pd.DataFrame()

comlist = serial.tools.list_ports.comports() #finds barcode port and opens it
connected = []
for element in comlist:
    connected.append(element.device)
    if element.description == "barcode scanner":
        ser = serial.Serial(element.device)
    print("Barcode Scanner connected at:", ser.name)

def storeVisit(student): #Keeps a list of all recorded scans
        visitHistory["studentID"].append(student["studentID"])
        visitHistory["name"].append(student["name"])
        visitHistory["major"].append(student["major"])
        visitHistory["Sign-in Time"].append(student["Sign-in Time"])
        visitHistory["Sign-out Time"].append(student["Sign-out Time"])
        
def signingIn(student): #Keeps a list of all recorded scans
        #edit students scan status and time
        student["Sign-in Time"] = datetime.datetime.now().time()
        student['signingIn'] = "False"
        print("Student Signed In!")
        
def signingOut(student): #Keeps a list of all recorded scans
        #edit students scan status and histoyr
        student["Sign-out Time"] = datetime.datetime.now().time()
        #record visit
        student['signingIn'] = "True"
        print("Student Signed Out :(")

def getStudent(line):
    #find student with matching ID
    for student in studentRecord:
        if student["studentID"] == line:
            return student
        else:
            print("Student Not Found")
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
                        student = studentRecord.loc[studentRecord['studentID'] == line]
                        ser.flush()
                        print("\n\nName",student.name,"\n\n")
                        if str(student['signingIn']) == "True": #If student is signing in
                            signingIn(student)
                        else: #If student is signing out
                            signingOut(student)
                            storeVisit(student)
                        #If time is pass hours
                        
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