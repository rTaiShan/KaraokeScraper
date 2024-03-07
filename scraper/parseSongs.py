from bs4 import BeautifulSoup
import re
import json

def get_songs():
    try:
        with open('musicas.json', 'rb') as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError): 
        data = parseSongs()
        with open('musicas.json', 'w+') as f:
            json.dump(data, f, indent=4)

    return data


def parseSongs():
    with open('musicas.html', 'rb') as fp:
        soup = BeautifulSoup(fp, 'html.parser')

    tables = soup.body.find_all('table')
    data_rows = []
    for table in tables:
        data_rows += table.find_all('tr')[1:]

    data = []
    for row in data_rows:
        columns = row.find_all('td')
        if len(columns) == 5:
            data.append(dict(
                artist=re.sub(r'\s+', ' ', columns[0].p.text).strip(),
                id=int(columns[1].p.text.strip()),
                title=re.sub(r'\s+', ' ', columns[2].p.text).strip(),
                lyricsPreview=re.sub(r'\s+', ' ', columns[3].p.text).strip(),
                language=columns[4].p.text.strip(),
            ))
        elif len(columns) == 4:
            first_column_split = columns[0].p.text.split()
            data.append(dict(
                artist=re.sub(r'\s+', ' ', ' '.join(first_column_split[:-1])).strip(),
                id=int(first_column_split[-1]),
                title=re.sub(r'\s+', ' ', columns[1].p.text).strip(),
                lyricsPreview=re.sub(r'\s+', ' ', columns[2].p.text).strip(),
                language=columns[3].p.text.strip(),
            ))
        elif len(columns) == 3:
            first_column_split : list[str] = columns[0].p.text.split()
            id_candidates = [e for e in first_column_split if e.isnumeric()]

            # TODO Handle ambiguous row (manual resolution or ..?)
            if len(id_candidates) != 1:
                print(f"Ambiguous row: {row}, skipping")
                continue
            song_id = id_candidates[0]

            artist = ' '.join(first_column_split[:first_column_split.index(song_id)])
            title = ' '.join(first_column_split[first_column_split.index(song_id) + 1:])

            data.append(dict(
                artist=artist,
                id=int(song_id),
                title=title,
                lyricsPreview=re.sub(r'\s+', ' ', columns[1].p.text).strip(),
                language=columns[2].p.text.strip(),
            ))
        else:
            print(columns)
            raise ValueError('Unexpected columns length')
    return data


def main():
    get_songs()


if __name__ == '__main__':
    main()
