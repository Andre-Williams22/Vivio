from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime
import os
import stripe
from dotenv import load_dotenv
load_dotenv()
from twilio.rest import Client



host = os.environ.get('MONGODB_URI', 'mongodb://localhost:27017/Movie')
client = MongoClient(host=f'{host}?retryWrites=false')
db = client.get_default_database()

# Creates MongoDB  Collection
movies = db.movies
comments = db.comments

app = Flask(__name__)

# Use if I were to go live
'''
secret_key = os.getenv("secret_key")
publishable_key = os.getenv("publishable_key")
'''
account_sid = 'AC1e5cce5f981923f34e5d2309d9a70cbb' #os.environ["account_sid"]
auth_token = '6ff543682f94c8de705d04f5f3c1768e' #os.environ['auth_token']
client = Client(account_sid, auth_token)

stripe_keys = {
  'secret_key': 'sk_test_S1UKtrSKbTVMv7YzQpch6RBc007RPTTUgW',
  'publishable_key': 'pk_test_LqQaKSR0V30253rAvgA8Bcd300FMsyQ5d2'
}


stripe.api_key = stripe_keys['secret_key']

@app.route('/')
def movies_index():
    '''Show all movies'''
    return render_template('movies_index.html', movies=movies.find(),
     key=stripe_keys['publishable_key'])


@app.route('/movies', methods=['POST'])
def movies_submit():
    '''Submit a new movie'''
    movie = {
        'title': request.form.get('title'),
        'ratings': request.form.get('ratings'),
        'description': request.form.get('description'),
        'videos': request.form.get('videos').split(),
        'created_at': datetime.now()
    }
    
    
    movie_id = movies.insert_one(movie).inserted_id
    return redirect(url_for('movies_show', movie_id=movie_id))


@app.route('/movies/<movie_id>')
def movies_show(movie_id):
    """Show a single movie."""
    movie = movies.find_one({'_id': ObjectId(movie_id)})
    movie_comments = comments.find({'movie_id': ObjectId(movie_id)})
    return render_template('movies_show.html', 
    movie=movie, comments=movie_comments)


@app.route('/movies/<movie_id>', methods=['POST'])
def movies_update(movie_id):
    '''Submit an edited movie'''
    updated_movie = {
        'title': request.form.get('title'),
        'description': request.form.get('description'),
        'videos': request.form.get('videos').split()
    }
    movies.update_one(
        {'_id': ObjectId(movie_id)},
        {'$set': updated_movie})
    return redirect(url_for('movies_show', movie_id=movie_id))


@app.route('/movies/new')
def movies_new():
    '''Create a new movie'''
    return render_template('movies_new.html', movie={}, title='New Movie')


@app.route('/movies/<movie_id>/edit')
def movies_edit(movie_id):
    '''Show the edit form for a movie'''
    movie = movies.find_one({'_id': ObjectId(movie_id)})
    return render_template('movies_edit.html', movie=movie, 
                            title='Edit Movie')


@app.route('/movies/<movie_id>/delete', methods=['POST'])
def movies_delete(movie_id):
    '''Delete one movie'''
    movies.delete_one({'_id': ObjectId(movie_id)})
    return redirect(url_for('movies_index'))


@app.route('/movies/comments', methods=['POST'])
def comments_new():
    """Submit a new comment."""
    comment = {
        'title': request.form['title'],
        'content': request.form['content'],
        'movie_id': ObjectId(request.form.get('movie_id'))
    }
    
    comment_id = comments.insert_one(comment).inserted_id
    return redirect(url_for('movies_show', movie_id=comment['movie_id']))


@app.route('/movies/comments/<comment_id>', methods=['POST'])
def comments_delete(comment_id):
    """Action to delete a comment."""
    comment = comments.find_one({'_id': ObjectId(comment_id)})
    comments.delete_one({'_id': ObjectId(comment_id)})
    return redirect(url_for('movies_show', movie_id=comment.get('movie_id')))

@app.route('/charge/message')
def show_message():
    ''' Shows the charge amount'''
    amounts=1000


    return render_template('charge.html', amount=amounts)

@app.route('/charge', methods=['POST'])
def charge():
    '''charges the user'''
    client = Client(account_sid, auth_token)
    message = client.messages \
        .create(
            body="Thank you for your purchase. Keep breathing!",
            from_='+12162086503',
            to='2142846514')
    print(message.sid)

    # amount in cents
    amount = 1000

    customer = stripe.Customer.create(
        email='sample@customer.com',
        source=request.form['stripeToken']
    )

    stripe.Charge.create(
        customer=customer.id,
        amount=amount,
        currency='usd',
        description='Flask Charge'
    )
    
    return redirect(url_for('show_message'))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=os.environ.get('PORT', 5000))