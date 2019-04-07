#!/usr/bin/env python3
# -*- coding: utf8 -*-
import RPi.GPIO as GPIO
import MFRC522_GPIOBCM
import signal
import pygame
import time
import Adafruit_SSD1306
from PIL import Image

"""
Mandarine
GPIO dans l'espace BCM
"""
class Mandarine:
    """Classe qui définit une mandarine complete
    Les attributs sont:
    _le numero de version
    _le display
    _le mixer est celui de pygame, accessible via pygame.mixer
    """
    def __init__(self):
        self.version = 0.1
        self.disp = Adafruit_SSD1306.SSD1306_128_64(rst=24)
        # Raspberry Pi pin configuration:
        self.disp.begin()
        # Clear display.
        self.disp.clear()
        self.disp.display()
        #Add interrupt on GPIO_23
        GPIO.setup(23, GPIO.IN, pull_up_down = GPIO.PUD_UP)
        GPIO.add_event_detect(23, GPIO.FALLING, callback=self.nextDir, bouncetime=300)
# au cas ou  if GPIO.event_detected(channel):
#                print('Bouton enfoncé')
        self.prologue()

    def nextDir(self, channel):
        print('channel:'+str(channel))
        print('self.nextDir() a faire')

    def bienvenue(self):
        image = Image.open('media/img/bienvenue.ppm').convert('1')
        self.disp.image(image)
        self.disp.display()
        pygame.init()
        pygame.mixer.init()
        pygame.mixer.music.load("media/messages/b.wav")
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pass
        # Clear display.
        self.disp.clear()
        self.disp.display()
        return

    def prologue(self):
        #on joue un son de bienvenue
        # et on affiche une jolie image
        self.bienvenue()

    def main(self):
        continue_reading = True
        signal.signal(signal.SIGINT, self.end_read)
        MIFAREReader = MFRC522_GPIOBCM.MFRC522()
    
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
    def end_read(self,signal,frame):
         global continue_reading
         print ("Lecture terminée")
         continue_reading = False
         GPIO.cleanup()


if __name__ == '__main__':
    mandarine = Mandarine()
    mandarine.main()

