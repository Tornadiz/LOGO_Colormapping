#!/usr/bin/env python3
# rpi_ws281x library Colormapping
# Author: Norbert Karpen
#
# To map specific LED strip locations to a color gradient
# 

import time
from rpi_ws281x import *
import argparse
from cv2 import imread
import numpy as np
from os import getcwd
from loc import locations

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
gradient = "gradient_logo_small.jpg"
gradient_2 = "gradient_logo_2_small.jpg"
speed = 100   # in %

def illuminate_all_pos(calc_colors):
        for [pos, col] in calc_colors:
                strip.setPixelColor(pos, Color(col[0], col[1], col[2]))
        strip.show()   

# color gradient mapping function
def colormap(strip, img_gradient, locations, shift, brightness):   
    calc_color = []    
    for j, (x, y) in enumerate(locations):
#         print("img_gradient[x, y]: ", img_gradient[x, y])
        
        B = int(img_gradient[x, y][0])
        G = int(img_gradient[x, y][1])
        R = int(img_gradient[x, y][2])
        color = (R, G, B)
        
        current_LED_num = j + shift        
        
        if current_LED_num > LED_COUNT-1: 
            current_LED_num = current_LED_num % LED_COUNT
        calc_color.append([current_LED_num, color])
        
    return calc_color   


# fade between colors     
def fade_gradient(strip, col_map_1, col_map_2, locations, speed):   
    fade_dist =  30
    for counter in range(0, fade_dist):
        col_map_inter = []
        for led_count, _ in enumerate(col_map_1):
                R_inter = int(col_map_1[led_count][1][0] + counter/fade_dist*(col_map_2[led_count][1][0] - col_map_1[led_count][1][0]))
                G_inter = int(col_map_1[led_count][1][1] + counter/fade_dist*(col_map_2[led_count][1][1] - col_map_1[led_count][1][1]))
                B_inter = int(col_map_1[led_count][1][2] + counter/fade_dist*(col_map_2[led_count][1][2] - col_map_1[led_count][1][2]))
                ins = [col_map_1[led_count][0], (R_inter, G_inter, B_inter)]
                col_map_inter.append(ins)
        illuminate_all_pos(col_map_inter)
        time.sleep(0.5/(speed/100))
        
        
# gradient animation functions      
def rotate_gradient(strip, img_gradient, locations, speed):
    bright = 255
    for k in range(0, LED_COUNT):
        col_map_new = colormap(strip, img_gradient, locations, k, bright)
        if k > 0:
                col_map_old = colormap(strip, img_gradient, locations, k-1, bright)        
                fade_gradient(strip, col_map_old, col_map_new, locations, speed*5)
#                 illuminate_all_pos(color_map)
                time.sleep(0.5/(speed/100))
        
        
# # Define functions which animate LEDs in various ways.
def colorWipe(strip, color, wait_ms=50):
    """Wipe color across display a pixel at a time."""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(wait_ms/1000.0)

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


    # theaterChase(strip, Color(127, 127, 127))  # White theater chase

        
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
    
    path_mainfolder = getcwd()
    try:
        grad_img_folder = path_mainfolder + "/" + gradient
        grad_img_2_folder = path_mainfolder + "/" + gradient_2
        image_grad = imread(grad_img_folder)
        image_grad_2 = imread(grad_img_2_folder)
        col_map_1 = colormap(strip, image_grad, locations, k, bright)
        col_map_2 = colormap(strip, image_grad_2, locations, k, bright)
        while True:
#             if i > len(gradient_li):
#                 i = 0
            
#             image_grad = cv2.imread(gradient_li(i))
            
        
                  # theaterChase(strip, Color(127, 127, 127))  # White theater chase

#             print ('gradient_list(' + str(i) + ') now playing')
        
            rotate_gradient(strip, image_grad, locations, speed)

            fade_gradient(strip, col_map_1, col_map_2, locations, speed)
            fade_gradient(strip, image_grad_2, image_grad, locations, speed)
#             i =+ 1

    except KeyboardInterrupt:
        if args.clear:
            colorWipe(strip, Color(0,0,0), 10)
