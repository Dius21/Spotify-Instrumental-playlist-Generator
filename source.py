import spotipy
from spotipy.oauth2 import SpotifyOAuth  
import re
import subprocess as x
import time

#The api keys have been removed from this source code so it is not going to be functional.
#You can get key and secret from spotify developers webpage and copy paste it.

#authentication -- User OAuth2
scope = "playlist-read-private playlist-read-collaborative playlist-modify-private playlist-modify-public user-library-modify user-library-read"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="YOUR_SPOTIFY_CLIENT_ID", client_secret="YOUR_SPOTIFY_CLIENT_SECRET", scope=scope, redirect_uri="http://localhost:8080"))

#getting the tracks
playlist_uri = input("Enter link to playlist:").split("/")[-1].split("?")[0]
x.call('cls',shell=True)
print("Getting Tracks from Playlist")
all_tracks= sp.playlist_tracks(playlist_uri)
playlist_tracks_temp = all_tracks["items"]
while all_tracks['next']:
        all_tracks = sp.next(all_tracks)
        playlist_tracks_temp.extend(all_tracks['items'])
all_track_names = [x["track"]["name"] for x in playlist_tracks_temp]


#get list of instrumentals
list_of_instrumentals_URLs=[]
c=0
c_found=0
c_not_found=0
for i in range(len(all_track_names)):
    _= sp.search(q=f'track:{all_track_names[i]} instrumental', type='track')
    search_result = _['tracks']['items']
    if search_result != []:
        if search_result != None:
            c_found+=1
            list_of_instrumentals_URLs.append("https://open.spotify.com/track/"+re.search(r"spotify:track:(.*)",search_result[0]['uri']).group(1))
        else:
            c_not_found+=1
    else:
        c_not_found+=1
    x.call('cls',shell=True)
    c+=1
    if (c%4)==1:
        print(f"Searching \\\nNumber of instrumentals found: {c_found}\nNumber of instrumentals not found: {c_not_found}")
    elif (c%4)==2:
        print(f"Searching |\nNumber of instrumentals found: {c_found}\nNumber of instrumentals not found: {c_not_found}")
    elif (c%4)==3:
        print(f"Searching /\nNumber of instrumentals found: {c_found}\nNumber of instrumentals not found: {c_not_found}")
    elif (c%4)==0:
        print(f"Searching -\nNumber of instrumentals found: {c_found}\nNumber of instrumentals not found: {c_not_found}")
x.call('cls',shell=True)
print(f"Number of instrumentals found: {c_found}\nNumber of instrumentals not found: {c_not_found}\nTotal searched = {c_found+c_not_found}")

#splitting large lists
i=0
dict_of_instrumental_URLs_split = {}
if len(list_of_instrumentals_URLs) > 100:
    while len(list_of_instrumentals_URLs) > 0:
        dict_of_instrumental_URLs_split[i] = list_of_instrumentals_URLs[0:100]
        del list_of_instrumentals_URLs[0:100]
        i+=1

#create playlist
userid=sp.current_user()['id']
sp.user_playlist_create(user=userid, name=f"Instrumental - {str(sp.playlist(playlist_id=playlist_uri, fields='name')['name'])}", public=False, collaborative=False, description='Hey! This playlist was auto-generated using Python and Spotipy library.')
playlists = sp.current_user_playlists(limit=5, offset=0)
playlist_id = playlists['items'][00]['id']
if i == 0:
    sp.playlist_add_items(playlist_id=playlist_id, items=list_of_instrumentals_URLs, position=None)
else:
    c=i
    while i>0:
        sp.playlist_add_items(playlist_id=playlist_id, items=dict_of_instrumental_URLs_split[c-i], position=None)
        i-=1

print("Playlist Created (Check your library)")
print("This window will close in 5 seconds.")
time.sleep(5)
