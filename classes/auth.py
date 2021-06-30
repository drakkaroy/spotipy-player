import os
import spotipy
import spotipy.util as util
import json
from json.decoder import JSONDecodeError
from datetime import datetime


class Auth:
    def __init__(self, username):
        self.username = username
        self.scope = 'user-read-private user-read-playback-state user-modify-playback-state'
        self.cache_file = f'.cache-{self.username}'

    def validate_token_expires(self):
 
        f = open(self.cache_file, "r")
        data = f.read()
        json_data = json.loads(data)
        timestamp_expires_date = json_data['expires_at']
        expires_date = datetime.fromtimestamp(timestamp_expires_date)
        print(expires_date)
        now = datetime.now()
        return expires_date > now

    def create_token(self):
        try:
            token = util.prompt_for_user_token(self.username, self.scope)
        except (AttributeError, JSONDecodeError):
            os.remove(self.cache_file)
            token = util.prompt_for_user_token(self.username, self.scope)

        return spotipy.Spotify(auth=token)
