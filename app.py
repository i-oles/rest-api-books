from flask import Flask, abort
from tinydb import TinyDB, Query
from collections import OrderedDict
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
    return {'all books' : db.all()}


def is_key_exist(book, key):
    try:
        return book['volumeInfo'][key]
    except:
        return None
    

@app.route('/books/<bookId>')
def get_book(bookId):
    b = Query()
    if db.contains(b.id == bookId):
        book = dict(db.get(b.id == bookId))
        return {'title' : is_key_exist(book, 'title'),
                'authors' : is_key_exist(book, 'authors'),
                'published_date' : is_key_exist(book, 'publishedDate'),
                'categories' : is_key_exist(book, 'categories'),
                'average_rating' : is_key_exist(book, 'average_rating'),
                'ratings_count' : is_key_exist(book, 'ratings_count'),
                'thumbnail' : is_key_exist(book, 'thumbnail')
                }
    else:
        return abort(404)

def all_keys_in_book(book):
    book = OrderedDict(book)
    keys = book.keys()
    values = book.values()
    all_fields = dict(zip(keys, values))
    return all_fields


@app.route('/books/posted')
def post_book(arg=''):
    b = Query()
    for book in items:
        if db.contains(b.id == book['id']):
            db.upsert(all_keys_in_book(book), b.id == book['id'])
            print('all data updated correctly')
        else:
            db.insert(all_keys_in_book(book))
            print('all data added correctly')
    return {'all books' : db.all()}


if __name__ == '__main__':
    app.run(debug=True)