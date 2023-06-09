#!/usr/bin/env python3
from smbus_ssd1306 import SSD1306_128_64
from PIL import Image, ImageDraw, ImageFont
import gpiod
import serial
import serial.tools.list_ports
import json
import time

buttons=[13,12,14] # P8_11, P8_12, P8_16
leds = [18,16,19] # P9_14, P9_15, P9_16


CONSUMER='getset'
CHIP='1'

YELLOW_LIMIT = 1
RED_LIMIT = 2

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


def cycleSRT(current:str, direction:int):
    #direction is int, +1 or -1 hopefully
    # set up srt list
    SRT_list = list(SRT_occupancy)
    # find where current SRT is
    index = SRT_list.index(current)
    # if else to handle ends of list
    length = len(SRT_list)
    if index == 0:
        if direction == -1:
            srt = SRT_list[-1]
            return srt
    elif index == length-1:
        if direction == 1:
            srt = SRT_list[0]
            return srt
    srt = SRT_list[index+direction]
    return srt

def main():
    chip = gpiod.Chip(CHIP)
    # set up gpio lines
    getlines = chip.get_lines(buttons)
    getlines.request(consumer=CONSUMER, type=gpiod.LINE_REQ_EV_BOTH_EDGES)

    setlines = chip.get_lines(leds)
    setlines.request(consumer=CONSUMER, type=gpiod.LINE_REQ_DIR_OUT)
    # Initialize display library.
    # 128x64 display with hardware I2C:
    disp = SSD1306_128_64()
    disp.begin()

    # Get display width and height.
    width = disp.width
    height = disp.height

    # Clear display.
    disp.clear()
    disp.display()

    # Create image buffer.
    # Make sure to create image with mode '1' for 1-bit color.
    image = Image.new('1', (width, height))

    # Load default font.
    font = ImageFont.load_default()

    # Create drawing object.
    draw = ImageDraw.Draw(image)

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
            input = getlines.event_wait(sec=1)
            if input:
                vals =  getlines.get_values()
                if vals[1] == 1:# center button pressed
                    pass
                elif vals[0] == 1: #left button pressed
                    current_SRT = cycleSRT(current_SRT, -1)
                elif vals[2] == 1: # right button pressed
                    current_SRT = cycleSRT(current_SRT, 1)
            occupancy = len(SRT_occupancy[current_SRT])
            if occupancy < YELLOW_LIMIT:
                setlines.set_values([0,0,1])
            elif occupancy >= YELLOW_LIMIT and occupancy < RED_LIMIT:
                setlines.set_values([0,1,0])
            elif occupancy >= RED_LIMIT:
                setlines.set_values([1,0,0])
            # first line
            draw.rectangle([0,0,disp.width,disp.height], fill=0)
            draw.text((0,0), "Select SRT to visit", font=font,fill=255)
            draw.text((0,16), current_SRT, font=font,fill=255)
            disp.image(image)
            disp.display()
    except KeyboardInterrupt:
        print("\n Shutting down scanner")
        ser.close()
        print("Exiting")


main()