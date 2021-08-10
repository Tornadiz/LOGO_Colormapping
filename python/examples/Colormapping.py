#!/usr/bin/env python3
# rpi_ws281x library Colormapping
# Author: Norbert Karpen
#
# To map specific LED strip locations to a color gradient
# 

import time
from rpi_ws281x import *
import argparse
import cv2

# LED strip configuration:
LED_COUNT      = 149      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

# Gradient settings

# gradient_li = ["gradient_logo.jpg"]
gradient = "/gradient_logo.jpg"
speed = 100                                         # in %
locations = [(1147,918),(385,1139),(627,841),(819,1321),(1254,939),(364,145),(392,748),(96,1167),(703,1029),(516,173),(145,573),
                (455,818),(281,258),(1237,1269),(555,1249),(86,296),(1242,228),(41,863),(453,387),(225,102),(32,785),
                (462,819),(1241,89),(212,1388),(739,1100),(1116,1587),(683,944),(1163,1564),(894,1096),(1268,1529),
                (846,653),(936,1533),(550,209),(1167,1495),(1252,1521),(706,361),(1213,1346),(1080,205),(975,1067),(171,1289),
                (350,958),(692,925),(1129,385),(784,1381),(403,1474),(559,339),(1155,578),(75,863),(897,1092),(443,1461),(422,1565),
                (192,1127),(1108,840),(701,1087),(592,387),(255,756),(579,1303),(944,1566),(463,1396),(125,922),(875,264),
                (367,1175),(214,132),(377,1327),(427,1582),(918,1439),(489,1402),(736,1270),(487,780),(98,112),(62,1167),
                (1061,872),(418,1553),(944,970),(589,673),(118,361),(814,550),(785,689),(888,1284),(463,1381),(378,903),
                (844,602),(692,394),(792,514),(409,131),(88,512),(695,1251),(1252,103),(421,1489),(761,419),(45,748),
                (1042,294),(958,706),(676,1607),(1217,1183),(288,829),(938,1125),(691,664),(349,430),(1113,327),(156,4),
                (1183,1345),(920,1050),(809,359),(444,282),(1147,1322),(715,1614),(300,1659),(491,912),(943,1112),(77,1334),
                (473,856),(536,1673),(174,533),(912,725),(431,1101),(915,982),(164,1405),(1192,616),(936,1032),(492,1506),
                (52,1037),(529,1548),(854,429),(569,288),(365,156),(75,1237),(1159,450),(482,1539),(492,19),(454,1626),
                (937,1315),(864,1311),(242,1269),(223,156),(1097,1334),(1152,1299),(384,1216),(996,868),(215,776),
                (4,1662),(1085,820),(1171,1328),(162,1432),(844,41),(461,239),(513,1420),(926,1167)]
# color gradient mapping function
def colormap(img_gradient, locations, shift, brightness):   
        
    for j, (x, y) in enumerate(locations):
        color = int(image[x, y])
        current_LED_num = j + shift
        if current_LED_num > 149: 
            current_LED_num = 149 - (j + shift)
        strip.setPixelColor(current_LED_num, color)
        
# gradient animation functions      
def rotate_gradient(img_gradient, locations, speed):
    bright = 255
    for k in LED_COUNT:        
        colormap(img_gradient, locations, k, bright)
        time.sleep(0.5*speed)              
        
        
# # Define functions which animate LEDs in various ways.
# def colorWipe(strip, color, wait_ms=50):
#     """Wipe color across display a pixel at a time."""
#     for i in range(strip.numPixels()):
#         strip.setPixelColor(i, color)
#         strip.show()
#         time.sleep(wait_ms/1000.0)

# def theaterChase(strip, color, wait_ms=50, iterations=10):
#     """Movie theater light style chaser animation."""
#     for j in range(iterations):
#         for q in range(3):
#             for i in range(0, strip.numPixels(), 3):
#                 strip.setPixelColor(i+q, color)
#             strip.show()
#             time.sleep(wait_ms/1000.0)
#             for i in range(0, strip.numPixels(), 3):
#                 strip.setPixelColor(i+q, 0)

# def wheel(pos):
#     """Generate rainbow colors across 0-255 positions."""
#     if pos < 85:
#         return Color(pos * 3, 255 - pos * 3, 0)
#     elif pos < 170:
#         pos -= 85
#         return Color(255 - pos * 3, 0, pos * 3)
#     else:
#         pos -= 170
#         return Color(0, pos * 3, 255 - pos * 3)

# def rainbow(strip, wait_ms=20, iterations=1):
#     """Draw rainbow that fades across all pixels at once."""
#     for j in range(256*iterations):
#         for i in range(strip.numPixels()):
#             strip.setPixelColor(i, wheel((i+j) & 255))
#         strip.show()
#         time.sleep(wait_ms/1000.0)

# def rainbowCycle(strip, wait_ms=20, iterations=5):
#     """Draw rainbow that uniformly distributes itself across all pixels."""
#     for j in range(256*iterations):
#         for i in range(strip.numPixels()):
#             strip.setPixelColor(i, wheel((int(i * 256 / strip.numPixels()) + j) & 255))
#         strip.show()
#         time.sleep(wait_ms/1000.0)

# def theaterChaseRainbow(strip, wait_ms=50):
#     """Rainbow movie theater light style chaser animation."""
#     for j in range(256):
#         for q in range(3):
#             for i in range(0, strip.numPixels(), 3):
#                 strip.setPixelColor(i+q, wheel((i+j) % 255))
#             strip.show()
#             time.sleep(wait_ms/1000.0)
#             for i in range(0, strip.numPixels(), 3):
#                 strip.setPixelColor(i+q, 0)

# Main program logic follows:
if __name__ == '__main__':
    # Process arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--clear', action='store_true', help='clear the display on exit')
    args = parser.parse_args()

    # Create NeoPixel object with appropriate configuration.
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    # Intialize the library (must be called once before other functions).
    strip.begin()

    print ('Press Ctrl-C to quit.')
    if not args.clear:
        print('Use "-c" argument to clear LEDs on exit')
    
    i=0
    try:
        
        while True:
            if i > len(gradient_li):
                i = 0
            
#             image_grad = cv2.imread(gradient_li(i))
            image_grad = cv2.imread(gradient)

            print ('gradient_list(' + str(i) + ') now playing')
        
            rotate_gradient(image_grad, locations, speed)
            
            i =+ 1

    except KeyboardInterrupt:
        if args.clear:
            colorWipe(strip, Color(0,0,0), 10)
