#!/usr/bin/env python

import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from time import sleep

reader = SimpleMFRC522()
GPIO.setwarnings(False)

spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(scope="user-modify-playback-state"))

ALBUMS = {
    "584192607192": "spotify:album:7FWCgfnTgupXdyBy51ME9m"
}

while True:
    try:
            id, _ = reader.read()
            if id in ALBUMS.keys():
                spotify.start_playback(context_uri=hm_uri)
    finally:
            GPIO.cleanup()
            sleep(10)
