#!/usr/bin/env python

import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from time import sleep
import logging
from datetime import datetime

reader = SimpleMFRC522()
GPIO.setwarnings(False)

spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(scope="user-modify-playback-state"))

ALBUMS = {
    584192607192: "spotify:album:7FWCgfnTgupXdyBy51ME9m"
}
APPLE_TV_ID = "6F2A5C54-CEB8-430F-A6B3-7E31DCE85846"

previous = 0

while True:
    try:
            id, _ = reader.read()
            logging.info(f"ID: {id}")
            if id in ALBUMS.keys() and id != previous:
                logging.info("Found album")
                spotify.transfer_playback(APPLE_TV_ID, False)
                spotify.start_playback(context_uri=ALBUMS[id])
                previous = id
    except Exception as e:
          logging.error(e)
    finally:
            GPIO.cleanup()
            sleep(2)
