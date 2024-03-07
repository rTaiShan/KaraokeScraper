import axios from 'axios'
import { DependencyList, useCallback, useEffect, useState } from 'react'
import './App.css'
import { ChevronDown, ChevronUp } from 'lucide-react'

function useDebounce(effect: any, dependencies: DependencyList, delay: number) {
  const callback = useCallback(effect, dependencies);

  useEffect(() => {
    const timeout = setTimeout(callback, delay);
    return () => clearTimeout(timeout);
  }, [callback, delay]);
}

interface Song {
  title: string,
  id: number,
  language: string,
  lyricsPreview: string,
  artist: string,
}

interface SearchResult {
  artist: string,
  songs: Song[]
}

function SongContainer({song} : {song: Song}) {
  return (
  <tr>
    <td>{song.id}</td>
    <td>{song.title}</td>
    <td>{song.lyricsPreview}</td>
    <td>{song.language}</td>
  </tr>
  )
}

function GenericArtistTile(
  {
    artist, 
    songs,
    isExpanded,
    setIsExpanded,
  }: {
    artist: string, 
    songs: Song[],
    isExpanded: boolean,
    setIsExpanded: (isExpanded: boolean) => void,
  }) {
  return (
    <div className='artist-tile'>
      <div className='artist-header'>
        <h3 className='artist-name'>{artist}</h3>
        <button
          className='expand-button'
          onClick={() => setIsExpanded(!isExpanded)}
        >
          {isExpanded ? <ChevronUp /> : <ChevronDown />}
        </button>
      </div>
      <div>
        { (isExpanded && songs.length > 0) &&
          <>
            <hr className='song-container-line'/>
            <table className='songs-container'>
              <tr>
                <th>Código</th>
                <th>Título</th>
                <th>Letra</th>
                <th>Idioma</th>
              </tr>
              {songs.map((song) => <SongContainer song={song}/>)}
            </table>
          </>
        }
      </div>
    </div>
  )
}

function ArtistTile({artist}: {artist: string}) {
  const [isExpanded, setIsExpanded] = useState<boolean>(false)
  const [songs, setSongs] = useState<Song[]>([]);

  useEffect(() => {
    if (!isExpanded) return;

    axios.get<Song[]>(`http://localhost:8000/songs/artist/${artist}`)
    .then((response) => setSongs(response.data))
    .catch((e) => console.error(e))
  }, [isExpanded])

  return <GenericArtistTile 
    artist={artist} 
    songs={songs} 
    isExpanded={isExpanded}
    setIsExpanded={setIsExpanded}
  />
}

function ResultsTile(
  {
    artist, 
    songs,
  }: {
    artist: string, 
    songs: Song[],
  }
) {
  const [isExpanded, setIsExpanded] = useState<boolean>(false)

  return <GenericArtistTile 
    artist={artist} 
    songs={songs} 
    isExpanded={isExpanded}
    setIsExpanded={setIsExpanded}
  />
}

function App() {
  const [artists, setArtists] = useState<string[]>([])
  const [searchValue, setSearchValue] = useState<string>('')
  const [searchResults, setSearchResults] = useState<SearchResult[]>([])

  useDebounce(() => {
    if (searchValue === '') return
    axios.get<SearchResult[]>(`http://localhost:8000/search/${searchValue}`)
    .then((response) => setSearchResults(response.data))
    .catch((e) => console.error(e))
  }, [searchValue], 500)

  useEffect(() => {
    axios.get<string[]>('http://localhost:8000/artists/all')
    .then((response) => setArtists(response.data))
    .catch((e) => console.error(e))
  }, [])

  return (
    <>
      <h1>Karaokê do Bar do Ivan</h1>
      <input 
        type="text" 
        id="search-input"
        placeholder='Busca por artista, título ou código.'
        onChange={(event) => {setSearchValue(event.target.value.toLowerCase().trim())}}
      />
      {
        searchValue === ''
        ? artists.map((artist) => <ArtistTile artist={artist}/>)
        : searchResults.map((result) => <ResultsTile artist={result.artist} songs={result.songs}/>)
      }
    </>
  )
}

export default App
