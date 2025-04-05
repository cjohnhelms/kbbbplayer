#!/usr/bin/env python

import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522, MFRC522
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
        # Scan for tags
        (status, TagType) = reader.MFRC522_Request(reader.PICC_REQIDL)

        # If a tag is found
        if status == reader.MI_OK:
            print("Tag detected")

            # Get the UID of the tag
            (status, uid) = reader.MFRC522_Anticoll()

            # If the UID is successfully obtained
            if status == reader.MI_OK:
                print("UID: " + ":".join([str(x) for x in uid]))

                # Select the tag
                reader.MFRC522_SelectTag(uid)

                # Read data from the tag
                data = [elem for index in [6] for elem in reader.MFRC522_Read(index)]
                result = ''.join([chr(charcode) for charcode in data])
                print("Data read:", result)
            else:
                print("Error obtaining UID")

except KeyboardInterrupt:
    print("Exiting...")
    reader.MFRC522_StopCrypto1()