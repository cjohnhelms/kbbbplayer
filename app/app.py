#!/usr/bin/env python

import RPi.GPIO as GPIO
from mfrc522 import MFRC522
from mfrc522 import SimpleMFRC522
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from time import sleep
import logging
from datetime import datetime

reader = MFRC522()
GPIO.setwarnings(False)

spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(scope="user-modify-playback-state"))

ALBUMS = {
    584192607192: "spotify:album:7FWCgfnTgupXdyBy51ME9m"
}

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

##while True:
##    try:
##            id, _ = reader.read()
##            if id in ALBUMS.keys():
##                logging.info("Found album")
##                spotify.start_playback(context_uri=ALBUMS[id])
##    finally:
##            GPIO.cleanup()
##            sleep(10)
