from flask import Flask, abort
from pysondb import db
import requests

"""
todo:
1. pyson adds additional id_field of database record 
2. POST -> change the route path and change source
3. 

"""


app = Flask(__name__)
db = db.getDb("db.json")

base_url = 'https://www.googleapis.com/books/v1/volumes?q=Hobbit'
data = requests.get(base_url).json()
items = data['items']


@app.route("/")
def home():
    return "<p>Hello, World!</p>"


@app.route('/books')
def get_all_books():
    return {'all books' : db.getAll()}


@app.route('/books/<bookId>')
def get_book(bookId):
    if db.getBy({'bookId':bookId}):
        book = db.getBy({'bookId':bookId})[0]
        return {
            'title' : book['title'],
            #'authors' : book['authors'],
            #'published_date' : book['publishedDate'],
            #'categories' : book['categories'],
            #'average_rating' : book['averageRating'],
            #'ratings_count' : book['ratingsCount'],
            #'thumbnail' : book['thumbnail']
            }
    else:
        return abort(404)


def all_fields_in_book(book):
    keys = book.keys()
    values = book.values()
    all_fields = dict(zip(keys, values))
    return all_fields


@app.route('/books/posted')
def post_book(arg=''):
    for book in items:
        if db.getBy({'bookId': book['id']}):
            db.updateById(book['id'], all_fields_in_book(book))
        else:
            db.add(all_fields_in_book(book))
    return {'all books' : db.getAll()}


if __name__ == '__main__':
    app.run(debug=True)