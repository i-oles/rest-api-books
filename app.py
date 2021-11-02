from flask import Flask, abort
from pysondb import db
import requests

app = Flask(__name__)
db = db.getDb("db.json")

base_url = 'https://www.googleapis.com/books/v1/volumes?q=Hobbit'
data = requests.get(base_url).json()
items = data['items']


@app.route("/")
def home():
    return "<p>Hello, World!</p>"


@app.route('/books')
def get_books():
    return db.getAll()


@app.route('/books/<bookId>')
def get_book(**kwargs):
    bookId = kwargs.get('bookId')

    if bookId:
        return base.get(bookId, None) or abort(404)
    else:
        pass

#some fields does not exist --> values to none

def parse_parameters(book):
    return {
        'bookId' : book['id'],
        'title' : book['volumeInfo']['title'],
        'authors' : book['volumeInfo']['authors'],
        'published_date' : book['volumeInfo'][''],
        'categories' : book['volumeInfo'],
        'average_rating' : book['volumeInfo'],
        'ratings_count' : book['volumeInfo'],
        'thumbnail' : book['volumeInfo']
        }


@app.route('/books/posted')
def post_book(arg=''):
    #todo base url + arg
    for book in items:
        if db.getBy({'bookId' : book['id']}):
            db.update(parse_parameters(book))
        else:
            db.add(parse_parameters(book))



if __name__ == '__main__':
    app.run(debug=True)