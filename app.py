from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId

client = MongoClient()
db = client.Movie
movies = db.movies


app = Flask(__name__)


@app.route('/')
def movies_index():
    """Show all movies."""
    return render_template('movies_index.html', movies=movies.find())

@app.route('/movies/new')
def movie_new():
    '''create a new movie '''
    return render_template('movies_new.html')

@app.route('/movies', methods=['POST'])
def movies_submit():
    """Submit a new movie"""
    movie = {
        'title': request.form.get('title'),
        'description': request.form.get('description'),
        'videos': request.form.get('videos').split()
    }
    movie_id = movies.insert_one(movie)
    return redirect(url_for('movies_index', movie_id=movie_id))

@app.route('/movies/<movie_id>')
def movies_show(movie_id):
    """Show a single playlist."""
    movie = movies.find_one({'_id': ObjectId(movie_id)})
    return render_template('movies_show.html', movie=movie)



if __name__ == '__main__':
    app.run(debug=True)