from fastapi import FastAPI
from fastapi.exceptions import HTTPException
from fastapi.middleware.cors import CORSMiddleware

from parseSongs import get_songs

songs = get_songs()
artists = sorted(list(set(e['artist'] for e in songs)))

artists_songs = {
    artist: [e for e in songs if e['artist'] == artist]
    for artist in artists 
} 

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:5173'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/songs/all")
def get_all_songs():
    return songs

@app.get('/artists/all')
def get_all_artists():
    return artists

@app.get('/artists/detailed')
def get_all_artists_with_songs():
    return artists_songs

@app.get('/songs/artist/{artist}')
def get_all_songs_by_artist(artist : str):
    try:
        return artists_songs[artist]
    except KeyError:
        raise HTTPException(status_code=404, detail="Artist not found")
    
@app.get('/search/{search_text}')
def search(search_text : str):
    search_text = search_text.lower().strip()

    artist_matches = [e for e in artists if search_text in e.lower()]
    results = [{
        'artist': artist,
        'songs': get_all_songs_by_artist(artist),
    } for artist in artist_matches]

    try:
        search_text_int = int(search_text)
        song_matches = [
            e for e in songs 
            if e['artist'] not in artist_matches and
            (search_text in e['title'].lower() or e['id'] == search_text_int)
        ]
    except ValueError:
        song_matches = [
            e for e in songs 
            if e['artist'] not in artist_matches and
            search_text in e['title'].lower()
        ]
    
    song_matches_artists = set([e['artist'] for e in song_matches])
    for artist in song_matches_artists:
        results.append({
            'artist': artist,
            'songs': [e for e in song_matches if e['artist'] == artist]
        })

    return results