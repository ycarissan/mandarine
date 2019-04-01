#!/usr/bin/env python3
# -*- coding: utf8 -*-
import RPi.GPIO as GPIO
import MFRC522
import signal
import pygame

def bienvenue():
   pygame.init()
#   pygame.mixer.init(frequency=8000, size=-16, channels=2, buffer=4096)
   pygame.mixer.init()
   pygame.mixer.music.load("media/messages/b.wav")
   pygame.mixer.music.play()
#   pygame.event.wait()
   while pygame.mixer.music.get_busy():
      pass
   return

def prologue():
   #on joue un son de bienvenue
   bienvenue()

def main():
   prologue()
   continue_reading = True
   signal.signal(signal.SIGINT, end_read)
   MIFAREReader = MFRC522.MFRC522()

   while true:
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

if __name__ == '__main__':
        main()

