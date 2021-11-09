from flask import Flask, request, json
from tinydb import TinyDB, Query
from collections import OrderedDict
from werkzeug.exceptions import HTTPException
import requests


app = Flask(__name__)
db = TinyDB('db.json', indent=4)


def map_book(book):
    return {'title' : book['volumeInfo'].get('title', None),
            'authors' : book['volumeInfo'].get('authors', None),
            'published_date' : book['volumeInfo'].get('publishedDate', None),
            'categories' : book['volumeInfo'].get('categories', None),
            'average_rating' : book['volumeInfo'].get('average_rating', None),
            'ratings_count' : book['volumeInfo'].get('ratings_count', None),
            'thumbnail' : book['volumeInfo'].get('thumbnail', None),
            }


@app.route("/books", methods=['GET'])
def get_books():

    query = Query().noop()
    
    author = request.args.getlist('author')
    if author:
        query = query & Query()['volumeInfo']['authors'].any(author)

    published_date = request.args.get('published_date')
    if published_date:
        query = query & Query().volumeInfo.publishedDate.search(published_date)


    unsorted_books = db.search(query)
    
    sort = request.args.get('sort')
    if sort == 'published_date':
        books = sorted(unsorted_books, key=lambda book: book['volumeInfo']['publishedDate'])
    elif sort == '-published_date':  
        books = sorted(unsorted_books, key=lambda book: book['volumeInfo']['publishedDate'], reverse=True)
    else:
        books = unsorted_books

    mapped_books = [map_book(book) for book in books]

    return {'books' : mapped_books}


@app.route('/books/<bookId>', methods = ['GET'])
def get_book(bookId):
    book = db.get(Query().id == bookId)
    if book:
        return map_book(book)
    else:
        return {'error' : 'not found'}


def all_keys_in_book(book):
    book = OrderedDict(book)
    keys = book.keys()
    values = book.values()
    all_fields = dict(zip(keys, values))
    return all_fields


@app.route('/db', methods=['POST'])
def add_books():
    data = request.get_json()
    q = data['q']
    content = requests.get('https://www.googleapis.com/books/v1/volumes', params={'q': q}).json()
    items = content['items']

    counter = {'added' : 0, 'updated' : 0}
    for book in items:
        if db.contains(Query().id == book['id']):
            db.upsert(all_keys_in_book(book), Query().id == book['id'])
            counter['updated'] += 1
        else:
            db.insert(all_keys_in_book(book))
            counter['added'] += 1

    return counter



# https://sites.uclouvain.be/P2SINF/flask/errorhandling.html
@app.errorhandler(HTTPException)
def handle_exception(e):
    response = e.get_response()
    response.data = json.dumps({
        "code": e.code,
        "name": e.name,
        "description": e.description,
    })
    response.content_type = "application/json"
    return response



if __name__ == '__main__':
    app.run(debug=True)