
from flask import Flask, render_template, request, redirect, url_for, session
import requests
import os

app = Flask(__name__)
app.secret_key = 'supersecreteprakharkey'

API_URL = "https://saavn.dev/api"

def fetch_data(endpoint, params=None):
    try:
        response = requests.get(f"{API_URL}/{endpoint}", params=params)
        if response.status_code == 200:
            return response.json()['data']
    except Exception as e:
        print(f"Error fetching {endpoint}: {e}")
    return []

@app.route('/')
def index():
    trending = fetch_data('songs/trending')
    new_releases = fetch_data('albums/new')
    return render_template('index.html', trending=trending, new_releases=new_releases)

@app.route('/search')
def search():
    query = request.args.get('q')
    results = fetch_data('search/songs', params={'query': query}) if query else []
    return render_template('search.html', results=results)

@app.route('/album/<id>')
def album(id):
    album_data = fetch_data(f'albums?id={id}')
    return render_template('album.html', album=album_data)

@app.route('/artist/<id>')
def artist(id):
    artist_data = fetch_data(f'artist?id={id}')
    return render_template('artist.html', artist=artist_data)

@app.route('/favorites')
def favorites():
    favorites = session.get('favorites', [])
    return render_template('favorites.html', favorites=favorites)

@app.route('/add_favorite', methods=['POST'])
def add_favorite():
    song = {
        'name': request.form['name'],
        'url': request.form['url']
    }
    favorites = session.get('favorites', [])
    favorites.append(song)
    session['favorites'] = favorites
    return redirect(url_for('favorites'))

@app.route('/playlist')
def playlist():
    playlist = session.get('playlist', [])
    return render_template('playlist.html', playlist=playlist)

@app.route('/add_playlist', methods=['POST'])
def add_playlist():
    song = {
        'name': request.form['name'],
        'url': request.form['url']
    }
    playlist = session.get('playlist', [])
    playlist.append(song)
    session['playlist'] = playlist
    return redirect(url_for('playlist'))

@app.route('/new_releases')
def new_releases():
    releases = fetch_data('albums/new')
    return render_template('new_releases.html', releases=releases)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
