#!/usr/bin/env python

import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from time import sleep
import logging
from datetime import datetime

#reader = SimpleMFRC522()
#GPIO.setwarnings(False)

#spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(scope="user-modify-playback-state"))

#ALBUMS = {
    #584192607192: "spotify:album:7FWCgfnTgupXdyBy51ME9m"
#}
#APPLE_TV_ID = "6F2A5C54-CEB8-430F-A6B3-7E31DCE85846"

#previous = 0

#try:
    #while True:
        #id, _ = reader.read()
        #logging.info(f"ID: {id}")
        #if id in ALBUMS.keys() and id != previous:
            #logging.info("Found album")
            #spotify.transfer_playback(APPLE_TV_ID, False)
            #spotify.start_playback(context_uri=ALBUMS[id])
            #previous = id
        #sleep(2)
#except KeyboardInterrupt:
        #GPIO.cleanup()
        #raise

reader = MFRC522()

try:
    while True:
        status, _ = reader.MFRC522_Request(reader.PICC_REQIDL)
        if status != reader.MI_OK:
            sleep(0.1)
            continue
        status, backData = reader.MFRC522_Anticoll()
        buf = reader.MFRC522_Read(0)
        reader.MFRC522_Request(reader.PICC_HALT)
        if buf:
            print(datetime.now().isoformat(), ':'.join([hex(x) for x in buf]))
finally:
        GPIO.cleanup()