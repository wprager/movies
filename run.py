from movies import app
import movies.controllers

if __name__ == "__main__":
	app.debug = True
	app.run()