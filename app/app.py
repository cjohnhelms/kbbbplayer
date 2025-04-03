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

while True:
    try:
            id, _ = reader.read()
            previous = id
            if id in ALBUMS.keys() and id != previous:
                logging.info("Found album")
                spotify.start_playback(context_uri=ALBUMS[id])
    finally:
            GPIO.cleanup()
            sleep(10)
