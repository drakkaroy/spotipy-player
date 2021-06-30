import os

class Utils:

    def env_vars_exist():
        if 'SPOTIPY_CLIENT_ID' in os.environ and 'SPOTIPY_CLIENT_SECRET' in os.environ and 'SPOTIPY_REDIRECT_URI' in os.environ:
            return True
        else:
            return False