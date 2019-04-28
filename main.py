#!/usr/bin/env python3
# -*- coding: utf8 -*-
import os
import logging
import RPi.GPIO as GPIO
import MFRC522_GPIOBCM
import signal
import pygame
import time
import Adafruit_SSD1306
from PIL import Image

logging.basicConfig(filename='message.debug', level=logging.DEBUG)
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
        self.mediadir="media/oli"
        self.loadMediaDir()
        self.iFile = -1
        #Add interrupt on GPIO_23
        GPIO.setup(23, GPIO.IN, pull_up_down = GPIO.PUD_UP)
        GPIO.add_event_detect(23, GPIO.FALLING, callback=self.playNext, bouncetime=300)
# au cas ou  if GPIO.event_detected(channel):
#                print('Bouton enfoncé')
        #init mixer
        pygame.init()
        pygame.mixer.init()
        self.prologue()

    def prologue(self):
        #on joue un son de bienvenue
        # et on affiche une jolie image
        self.bienvenue()

    def bienvenue(self):
        image = Image.open('media/img/bienvenue.ppm').convert('1')
        self.disp.image(image)
        self.disp.display()
        self.playFile("media/messages/b.wav")
        #on attend la fin du message de bienvenue
        while pygame.mixer.music.get_busy():
            pass
        # Clear display.
        self.disp.clear()
        self.disp.display()
        return
    
    def loadMediaDir(self):
        """
        Charge le repertoire contenant les media a proposer
        """
        self.playlist = list()
        for f in os.listdir(self.mediadir):
            self.playlist.append(self.mediadir + "/" + f)
        logging.info('Media:')
        logging.info('mediadir=%s',self.mediadir)
        i=0
        for filename in self.playlist:
           i=i+1
           logging.info('%i %s' , i , filename)

    def playNext(self, channel):
        self.stopPlaying()
        self.iFile = self.iFile+1
        if self.iFile>len(self.playlist):
            self.iFile=0
        filename=self.playlist[self.iFile]
        self.playFile(filename)

    def stopPlaying(self):
        pygame.mixer.music.stop()

    def playFile(self,filename):
        pygame.mixer.music.load(filename)
        pygame.mixer.music.play()

    def main(self):
        global continue_reading
        continue_reading = True
        signal.signal(signal.SIGINT, self.end_read)
        MIFAREReader = MFRC522_GPIOBCM.MFRC522()
    
        while continue_reading:
    # Detecter les tags
            (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)
    # Une carte est detectee
            if status == MIFAREReader.MI_OK:
                print ("Carte detectee")
                (status,uid) = MIFAREReader.MFRC522_Anticoll()
                print(uid)
                logging.info("Carte detectee %s", uid)
                if (uid[0]==33) and \
                   (uid[1]==194)and \
                   (uid[2]==2)  and \
                   (uid[3]==137)and \
                   (uid[4]==104):
                    self.mediadir="media/oli"
                elif (uid[0]==136)and \
                   (uid[1]==4)  and \
                   (uid[2]==103)and \
                   (uid[3]==112)and \
                   (uid[4]==155):
                    self.mediadir="media/Tintin_Le_Lotus_bleu"
                self.loadMediaDir()
                self.iFile=-1
                self.playNext(0)
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

