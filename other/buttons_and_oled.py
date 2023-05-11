#!/usr/bin/env python3
from smbus_ssd1306 import SSD1306_128_64
from PIL import Image, ImageDraw, ImageFont
import gpiod


buttons=[13,12,14] # P8_11, P8_12, P8_16
leds = [18,16,19] # P9_14, P9_15, P9_16


CONSUMER='getset'
CHIP='1'

chip = gpiod.Chip(CHIP)
# set up gpio lines
getlines = chip.get_lines(buttons)
getlines.request(consumer=CONSUMER, type=gpiod.LINE_REQ_EV_RISING_EDGE)

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


current_SRT = 0
SRT_list = ["placeholder 0", "placeholder 1", "placeholder 2"]
SRT_occupancy = [0,1,2]
try:    
    while True:
        input = getlines.event_wait()
        if input:
            vals =  getlines.get_values()
            if vals[1] == 1:# center button pressed
                pass
            elif vals[0] == 1: #left button pressed
                current_SRT -= 1
            elif vals[2] == 1: # right button pressed
                current_SRT += 1
            if current_SRT < 0: # reset upon reaching end of list
                current_SRT = len(SRT_list)+current_SRT
            elif current_SRT >= len(SRT_list):
                current_SRT = 0
        
        if SRT_occupancy[current_SRT] == 0:
            setlines.set_values([0,0,1])
        elif SRT_occupancy[current_SRT] == 1:
            setlines.set_values([0,1,0])
        elif SRT_occupancy[current_SRT] > 1:
            setlines.set_values([1,0,0])
        # first line
        draw.rectangle([0,0,disp.width,disp.height], fill=0)
        draw.text((0,0), "Select SRT to visit", font=font,fill=255)
        draw.text((0,16), SRT_list[current_SRT], font=font,fill=255)
        disp.image(image)
        disp.display()
except KeyboardInterrupt:
    exit(0)