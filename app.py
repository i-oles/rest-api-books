from flask import Flask, abort, render_template, request
from tinydb import TinyDB, Query, where
from collections import OrderedDict
import requests
import re

# Todo:

# less fields in db
# case insensitive
# author & author
# url correct paths
# keys names of returns
# all books view --> add context?
# two different authors

# venv/pyenv.cfg
# include-system-site-packages = true
    #sort = request.form.get('sort')


app = Flask(__name__)
db = TinyDB('db.json', indent=4)


@app.route("/books", methods=['GET'])
def get_books():
    author = request.args.get('author')
    if author:
        books_by_authors = db.search(where('volumeInfo')['authors'].any(author))
        return {f'written by {author}': books_by_authors}
    
    published_date = request.args.get('published_date')
    if published_date:
        books_by_date = db.search(Query().volumeInfo.publishedDate.search(published_date))
        return {f'published in {published_date}' : books_by_date}

    def myFunc(e):
        return e['volumeInfo']

    sort = request.args.get('sort')
    if sort == 'published_date':
        return db.all().sort(key=myFunc)
    if sort == '-published_date':
        return db.all().sort(reverse= True, key=lambda x: x['volumeInfo']['publishedDate'])

    return {'all books' : db.all() }


    """
    if request.method == 'GET':
        published_date = request.args.get('published_date')
        authors = request.args.get('authors')
    """
    


def all_keys_in_book(book):
    book = OrderedDict(book)
    keys = book.keys()
    values = book.values()
    all_fields = dict(zip(keys, values))
    return all_fields


@app.route('/db', methods=['POST'])
def add_books():
    q = requests.data=payload)
    d = 'https://www.googleapis.com/books/v1/volumes'

    data = requests.get(api_url).json()
    items = data['items']

    for book in items:
        if db.contains(Query().id == book['id']):
            db.upsert(all_keys_in_book(book), Query().id == book['id'])
        else:
            db.insert(all_keys_in_book(book))

    return { 'all books': db.all() }



@app.route('/books/<bookId>')
def get_book(bookId):
    if db.contains(Query().id == bookId):
        book = db.get(Query().id == bookId)
        return {'title' : book['volumeInfo'].get('title', None),
                'authors' : book['volumeInfo'].get('authors', None),
                'published_date' : book['volumeInfo'].get('publishedDate', None),
                'categories' : book['volumeInfo'].get('categories', None),
                'average_rating' : book['volumeInfo'].get('average_rating', None),
                'ratings_count' : book['volumeInfo'].get('ratings_count', None),
                'thumbnail' : book['volumeInfo'].get('thumbnail', None),
                }
    else:
        return abort(404) 


if __name__ == '__main__':
    app.run(debug=True)