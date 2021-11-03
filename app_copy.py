from flask import Flask, abort
from tinydb import TinyDB, Query
import requests


app = Flask(__name__)
db = TinyDB('db.json')

base_url = 'https://www.googleapis.com/books/v1/volumes?q=Hobbit'
data = requests.get(base_url).json()
items = data['items']


@app.route("/")
def home():
    return "<p>Hello, World!</p>"


@app.route('/books')
def get_all_books():
    db.insert({'bookId' : 'dddddd', 'title': 'abrakadabra', 'lastname' : 'oles'})
    return {'all books' : db.all()}


@app.route('/books/<bookId>')
def get_book(bookId):
    b = Query()
    if db.search(b.bookId == bookId):
        book = db.get(b.bookId == bookId)
        return {
            'title' : book['title'],
            #'authors' : book['authors'],
            #'published_date' : book['publishedDate'],
            #'categories' : book['categories'],
            #'average_rating' : book['averageRating'],
            #'ratings_count' : book['ratingsCount'],
            #'thumbnail' : book['thumbnail']
            }


def all_fields_in_book(book):
    keys = book.keys()
    values = book.values()
    all_fields = dict(zip(keys, values))
    return all_fields


@app.route('/books/posted')
def post_book(arg=''):
    b = Query()
    for book in items:
        if db.search(b.bookId == book['id']):

            ### finish here

            db.updateById(book['id'], all_fields_in_book(book))
        else:
            db.add(all_fields_in_book(book))
    return {'all books' : db.getAll()}


if __name__ == '__main__':
    app.run(debug=True)