#!/usr/bin/env python

import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
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
spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(scope="user-modify-playback-state"))

reader = SimpleMFRC522()

try:
    print("Place your RFID tag on the reader...")
    
    while True:
        id, _ = reader.read_no_block()  # Non-blocking read

        if id:
            print(id)
        
        if id and id in ALBUMS.keys() and id != previous:  # Tag detected
            logging.info("Album found")
            spotify.transfer_playback(APPLE_TV_ID, False)
            spotify.start_playback(APPLE_TV_ID, context_uri=ALBUMS[id])
        else:
            print("No tag detected.")
            spotify.pause_playback(APPLE_TV_ID)
        
        sleep(1)  # Wait a bit before checking again

except KeyboardInterrupt:
    print("Program terminated.")