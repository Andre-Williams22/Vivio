from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient

client = MongoClient()
db = client.Movie
movies = db.movies
'''
movies = [
    { 'title': 'Cat Videos', 'description': 'Cats acting weird' },
    { 'title': '80\'s Music', 'description': 'Don\'t stop believing!' }
]
'''

app = Flask(__name__)


@app.route('/')
def index():
    """return homepage"""
    return render_template('home.html')


@app.route('/movies')
def movies_index():
    """Show all movies."""
    return render_template('movies_index.html', movies=movies)





if __name__ == '__main__':
    app.run(debug=True)