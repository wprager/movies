from flask import Flask, render_template, request
from movies import app

import json
import urllib.parse
import urllib.request

API_KEY = '91f2119708320f8847a2f21999aab4f3'
API_URL = 'https://api.themoviedb.org/3/'

# ---------------------------------------
# ROUTES
# ---------------------------------------
@app.route('/')
def route_index():
	r = urllib.request.urlopen('{}movie/popular?api_key={}'.format(API_URL, API_KEY))
	popular_movies = json.loads(r.read()).get('results')
	return render_template('index.html', popular_movies=popular_movies)

@app.route('/movie/<movie_id>')
def route_movie(movie_id):
	r = urllib.request.urlopen('{}movie/{}?api_key={}'.format(API_URL, movie_id, API_KEY))
	movie = json.loads(r.read())
	return render_template('movie.html', movie=movie)

@app.route('/search')
def route_search():
	query = urllib.parse.quote(request.args.get('query'))
	r = urllib.request.urlopen('{}search/movie?api_key={}&query={}'.format(API_URL, API_KEY, query))
	movies = json.loads(r.read()).get('results')
	return render_template('search-results.html', movies=movies)