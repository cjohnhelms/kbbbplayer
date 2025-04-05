#!/usr/bin/env python

import RPi.GPIO as GPIO
from mfrc522 import MFRC522
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from time import sleep
import logging

ALBUMS = {
    "1364151195216": "spotify:album:7FWCgfnTgupXdyBy51ME9m"
}
APPLE_TV_ID = "6F2A5C54-CEB8-430F-A6B3-7E31DCE85846"

previous = 0

GPIO.setwarnings(False)
reader = MFRC522()
spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(scope="user-modify-playback-state"))

try:
    while True:
        # Scan for tags
        (status, TagType) = reader.MFRC522_Request(reader.PICC_REQIDL)

        # If a tag is found
        if status == reader.MI_OK:
            logging.info("Album detected")
            # Get the UID of the tag
            (status, uid) = reader.MFRC522_Anticoll()
            # If the UID is successfully obtained
            if status == reader.MI_OK:
                id = "".join([str(x) for x in uid])
                if id in ALBUMS.keys() and id != previous:
                    spotify.transfer_playback(APPLE_TV_ID, False)
                    spotify.start_playback(context_uri=ALBUMS[id])
                    previous = id
        else:
            logging.info("Album removed")
            spotify.pause_playback(APPLE_TV_ID)
        
        sleep(2)

except KeyboardInterrupt:
    print("Exiting...")
    reader.MFRC522_StopCrypto1()