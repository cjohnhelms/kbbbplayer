#!/usr/bin/env python

import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from time import sleep
import logging

logging.basicConfig(level = logging.INFO)

ALBUMS = {
    584192607192: "spotify:album:7FWCgfnTgupXdyBy51ME9m"
}
APPLE_TV_ID = "6F2A5C54-CEB8-430F-A6B3-7E31DCE85846"

previous = 0
no_tag = 0

GPIO.setwarnings(False)
spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(scope="user-modify-playback-state"))

reader = SimpleMFRC522()

try:
    print("Place your RFID tag on the reader...")
    
    while True:

        logging.info(f"no tag check: {no_tag}")

        if no_tag >= 3:
            spotify.pause_playback(APPLE_TV_ID)
            previous = 0

        id, _ = reader.read_no_block()  # Non-blocking read

        if id and id in ALBUMS.keys():
            logging.info("Album found")
            if id == previous:
                spotify.start_playback()
            else:
                spotify.transfer_playback(APPLE_TV_ID, False)
                spotify.start_playback(APPLE_TV_ID, context_uri=ALBUMS[id])
                previous = id
        else:
            no_tag += 1

        if id:
            logging.info("tag detected")
            no_tag = 0
        
        sleep(1)  # Wait a bit before checking again

except KeyboardInterrupt:
    print("Program terminated.")