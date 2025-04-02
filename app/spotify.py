import spotipy
from spotipy.oauth2 import SpotifyOAuth

ALBUMS = {
    "": "spotify:album:7FWCgfnTgupXdyBy51ME9m"
}

spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(scope="user-modify-playback-state"))

spotify.start_playback(context_uri=hm_uri)