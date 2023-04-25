import serial
import datetime
import serial.tools.list_ports

visitHistory = dict({"studentID":[], "name":[],"major":[],"Sign-in Time":[],"Sign-out Time":[]})
roomStatus = dict({"Studnets In":[]})

comlist = serial.tools.list_ports.comports() #finds barcode port and opens it
connected = []
for element in comlist:
    connected.append(element.device)
    if element.description == "barcode scanner":
        ser = serial.Serial(element.device)
    print("Barcode Scanner connected at:", ser.name)
    
def storeVisit(student): #Keeps a list of all recorded scans
        visitHistory["studentID"].append(student.id)
        visitHistory["name"].append(student.name)
        visitHistory["major"].apppend(student.major)
        visitHistory["Sign-in Time "].append(student.inTime)
        visitHistory["Sign-out Time "].append(student.outTime)
        
def signingIn(student): #Keeps a list of all recorded scans
        #edit students scan status and time
        student.inTime = datetime.datetime.now().time()
        
def signingOut(student): #Keeps a list of all recorded scans
        #edit students scan status and histoyr
        student.outTime = datetime.datetime.now().time()
        #record visit
        storeVisit(student)
        
def getStudent(line):
    #find student with matching ID
    for student in students:
        if student.id == line:
            return student
        else:
            print("Student Not Found")
            
while True: #checks for new input from barcode and updates dataframe
    line = ser.readline()
    line = line.decode('utf-8',errors='ignore').rstrip('/r/n')
    line = int(line)
    student = getStudent(line)
    if student.signingIn: #If student is signing in
        addSignIn(student)
        student.signingIn = False
    else: #If student is signing out
        addSignOut(student)
        student.signingIn = True
    #If time is pass hours
        for student in Students
