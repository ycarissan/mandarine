#!/usr/bin/env python3
# -*- coding: utf8 -*-
import RPi.GPIO as GPIO
import MFRC522
import signal
import pygame
import time
#import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306
from PIL import Image

def bienvenue():
   global disp
   image = Image.open('media/img/bienvenue.ppm').convert('1')
   disp.image(image)
   disp.display()
   pygame.init()
   pygame.mixer.init()
   pygame.mixer.music.load("media/messages/b.wav")
   pygame.mixer.music.play()
   while pygame.mixer.music.get_busy():
      pass
# Clear display.
   disp.clear()
   disp.display()
   return

def prologue():
   #on joue un son de bienvenue
   bienvenue()

def main():
   prologue()
   continue_reading = True
   signal.signal(signal.SIGINT, end_read)
   MIFAREReader = MFRC522.MFRC522()

   while True:
# Detecter les tags
      (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)
# Une carte est detectee
      if status == MIFAREReader.MI_OK:
         print ("Carte detectee")
# Recuperation UID
      (status,uid) = MIFAREReader.MFRC522_Anticoll()
      pass

# Fonction qui arrete la lecture proprement 
def end_read(signal,frame):
    global continue_reading
    print ("Lecture terminée")
    continue_reading = False
    GPIO.cleanup()

def configuration():
   global disp
   # Raspberry Pi pin configuration:
   RST = 24
   disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST)
   disp.begin()
# Clear display.
   disp.clear()
   disp.display()

if __name__ == '__main__':
   configuration()
   main()

