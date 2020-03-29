from flask import Flask, render_template, request
from movies import app

import functools
import json
import urllib.parse
import urllib.request

API_KEY = '91f2119708320f8847a2f21999aab4f3'
API_URL = 'https://api.themoviedb.org/3/'

genre_cache = {}
title_cache = {}

# ---------------------------------------
# ROUTES
# ---------------------------------------
@app.route('/')
@functools.lru_cache(maxsize=1)
def route_index():
	print('Cache miss, fetching popular titles.')
	r = urllib.request.urlopen('{}movie/popular?api_key={}'.format(API_URL, API_KEY))
	popular_movies = json.loads(r.read()).get('results')
	
	for movie in popular_movies:
		populate_genres(movie)
	
	return render_template('index.html', popular_movies=popular_movies)

@app.route('/movie/<movie_id>')
@functools.lru_cache(maxsize=100)
def route_movie(movie_id):
	print('Cache miss, fetching movie {}.'.format(movie_id))
	r = urllib.request.urlopen('{}movie/{}?api_key={}'.format(API_URL, movie_id, API_KEY))
	movie = json.loads(r.read())
	title_cache[movie_id] = movie.get('title')
	
	movie['genres'] = join_names(movie.get('genres'), 'name')
	movie['production_companies'] = join_names(movie.get('production_companies'), 'name')
	movie['production_countries'] = join_names(movie.get('production_countries'), 'name')
	movie['spoken_languages'] = join_names(movie.get('spoken_languages'), 'name')
	
	return render_template('movie.html', movie=movie)

@app.route('/movie/<movie_id>/similar')
@functools.lru_cache(maxsize=100)
def route_similar(movie_id):
	print('Cache miss, fetching movies similar to {}.'.format(movie_id))
	r = urllib.request.urlopen('{}movie/{}/similar?api_key={}'.format(API_URL, movie_id, API_KEY))
	movies = json.loads(r.read()).get('results')
	
	for movie in movies:
		populate_genres(movie)
	
	if not title_cache.get(movie_id):
		m = urllib.request.urlopen('{}movie/{}?api_key={}'.format(API_URL, movie_id, API_KEY))
		title = json.loads(m.read()).get('title')
		title_cache[movie_id] = title
	else:
		title = title_cache.get(movie_id)
	
	return render_template('similar.html', movies=movies, title=title, movie_id=movie_id)

@app.route('/search')
def route_search():
	query = urllib.parse.quote(request.args.get('query'))
	return render_template('search-results.html', movies=search_movies(query))

# ---------------------------------------
# UTIL
# ---------------------------------------
def populate_genres(movie):
	movie_genres = []
	
	if not genre_cache:
		r = urllib.request.urlopen('{}genre/movie/list?api_key={}'.format(API_URL, API_KEY))
		genres = json.loads(r.read()).get('genres')
		for genre in genres:
			genre_cache[genre.get('id')] = genre.get('name')
	
	genre_ids = movie.get('genre_ids')
	for genre_id in genre_ids:
		movie_genres.append(genre_cache.get(genre_id))
	
	movie['genres'] = ', '.join(movie_genres)

def join_names(items, field_name):
	name_list = [item[field_name] for item in items]
	return ', '.join(name_list)

@functools.lru_cache(maxsize=100)
def search_movies(query):
	print('Cache miss, fetching search for {}.'.format(query))
	r = urllib.request.urlopen('{}search/movie?api_key={}&query={}'.format(API_URL, API_KEY, query))
	movies = json.loads(r.read()).get('results')
	
	for movie in movies:
		populate_genres(movie)
	
	return movies
