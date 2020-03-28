from flask import Flask, request
from movies import app

import requests

# ---------------------------------------
# ROUTES
# ---------------------------------------
@app.route('/')
def route_index():
	return 'hello world'
