#!/usr/bin/env python3
from smbus_ssd1306 import SSD1306_128_64
from PIL import Image, ImageDraw, ImageFont


# 128x64 display with hardware I2C:
disp = SSD1306_128_64()

# Initialize library.
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

# first line
draw.text((0,0), "Select SRT to visit", font=font,fill=255)
disp.image(image)
disp.display()