import sys
import json
import webbrowser
from json.decoder import JSONDecodeError
from classes.auth import Auth
from utils import Utils

if not sys.argv[1:]:
    username = input('What is your username? ')
else:
    username = sys.argv[1]

if not Utils.env_vars_exist():
    print('You need setting the environment variables')
else:
    auth = Auth(username)
    spotifyObject = auth.create_token()

    # User information
    user = spotifyObject.current_user()
    nickname = user['display_name']

    # Getting Devices
    devices = spotifyObject.devices()
    # print(json.dumps(devices, sort_keys=True, indent=4))

    if len(devices['devices']) < 1:
        print('Is neccesary at least one Spotify app open')
    else:
        device_id = devices['devices'][0]['id']

        # Currrent user playing track
        track = spotifyObject.current_user_playing_track()
        # print(json.dumps(track, sort_keys=True, indent=4))
        if not track:
            print('Currently you are not playing any track.')
        else:
            artist = track['item']['artists'][0]['name']
            track = track['item']['name']
            print('You are currently playing => {} : {}'.format(artist, track))

        # Starting the game
        while True:

            print('0 - exit')
            print('1 - Search for an artist')

            choice = input('Your choice: ')

            if choice == '0':
                break

            if choice == '1':
                search_query = input('What do you want play? ')
                search_results = spotifyObject.search(
                    search_query, limit=50, offset=0, type='artist')

                artist = search_results['artists']['items'][0]
                artist_name = artist['name']
                artist_id = artist['id']

                print(f'Here you have the albums of {artist_name}')

                albums = spotifyObject.artist_albums(artist_id)
                albums = albums['items']

                album_list = []

                for index, item in enumerate(albums, start=1):
                    album_list.append({
                        'index': index,
                        'name': item['name'],
                        'id': item['id'],
                        'uri': item['uri']
                    })
                    print(
                        f'{index}. {item["name"]} : {item["release_date"]}')

                while True:
                    album_selection = input(
                        'Enter the number of the album and play it or (x to exit) ')

                    if album_selection == 'x':
                        break

                    selected = album_list[int(album_selection)-1]
                    tracks = spotifyObject.album_tracks(selected['id'])
                    tracks = tracks['items']

                    track_list = []
                    for item in tracks:
                        track_list.append(item['uri'])

                    spotifyObject.start_playback(
                        device_id, selected['uri'])

                    # play an album, just with the album uri
                    #
                    # spotifyObject.start_playback(
                    #     device_id, selected['uri'])

                    # play an playlist, with a track list,
                    # this not showing the list on the app
                    #
                    # spotifyObject.start_playback(
                    #     device_id, None, track_list)
