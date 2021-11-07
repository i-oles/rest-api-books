from flask import Flask, abort, render_template, request
from tinydb import TinyDB, Query, where
from collections import OrderedDict
import requests
import re

# Todo:

# less fields in db


# author & author
# filter with sort together

# 8. books list - only title?

# venv/pyenv.cfg
# include-system-site-packages = true
    #sort = request.form.get('sort')

    # TODO wybrać match/substring zamiast ==
    # books = db.search(where('volumeInfo')['q'] == q) if q else db.all()


    # &



app = Flask(__name__)
db = TinyDB('db.json')

base_url = 'https://www.googleapis.com/books/v1/volumes?q=Hobbit'
data = requests.get(base_url).json()
items = data['items']



@app.route("/books", methods=['GET', 'POST'])
def books():
    """
    if request.method == 'POST':
        authors = request.form.get('authors')
        books_by_authors = db.search(where('volumeInfo')['authors'].any(authors))

        return {'authors': books_by_authors}
    
    if request.method == 'POST':
        published_date = request.form.get('published_date')
        books_by_date = db.search(Query().volumeInfo.publishedDate.search(published_date))
        
        return {'authors': books_by_date}
    """

    return render_template('app/index.html')




def all_keys_in_book(book):
    book = OrderedDict(book)
    keys = book.keys()
    values = book.values()
    all_fields = dict(zip(keys, values))
    return all_fields


@app.route('/db', methods=['GET', 'POST'])
def add_books():
    if request.method == 'POST':
        q = request.form.get('q')
        api_url = 'https://www.googleapis.com/books/v1/volumes' + '?q=' + q

        data = requests.get(api_url).json()
        items = data['items']

        for book in items:
            if db.contains(Query().id == book['id']):
                db.upsert(all_keys_in_book(book), Query().id == book['id'])
                print('updated')
            else:
                db.insert(all_keys_in_book(book))
                print('added') 
        return { 'all books': db.all() }
    
    return render_template('app/add_books.html')






"""


def return_key_if_exist(book, key):
    try:
        return book['volumeInfo'][key]
    except:
        return None
    

@app.route('/books/<bookId>')
def get_book(bookId):
    if db.contains(Query().id == bookId):
        book = db.get(Query().id == bookId)
        return {'title' : return_key_if_exist(book, 'title'),
                'authors' : return_key_if_exist(book, 'authors'),
                'published_date' : return_key_if_exist(book, 'publishedDate'),
                'categories' : return_key_if_exist(book, 'categories'),
                'average_rating' : return_key_if_exist(book, 'average_rating'),
                'ratings_count' : return_key_if_exist(book, 'ratings_count'),
                'thumbnail' : return_key_if_exist(book, 'thumbnail')
                }
    else:
        return abort(404)




@app.route('/books', methods=['POST', 'GET'])
def filter_by_year():
    if request.method == 'POST':
        year = request.form['year']
        filtered_books = []
        for book in db.all():
            published_date = book['volumeInfo']['publishedDate']
            if published_date.startswith(year):
                filtered_books.append(book)   
    return {f'published in {year}' : [book for book in filtered_books]}


def raw_data(data):
    data = data.replace(',' , '')
    return data.strip()


@app.route('/books', methods=['POST', 'GET'])
def filter_by_authors():
    filtered_books = []

    def find_book_by_author(name):
        for book in db.all():
            author = book['volumeInfo']['authors']
            if name in author:
                filtered_books.append(book)

    if request.method == 'POST':
        authors = request.form['autors'].replace(',' , '')
        authors = [raw_data(author) for author in authors.split()]
        for author in authors:
            find_book_by_author(author)
    
    #return {f'written by {authors}' : [book for book in filtered_books]}
    return {f'written by {authors}' : filtered_books}


@app.route('/books/sort', methods=['POST', 'GET'])
def sort_by_date():
    ascending = True
    #if request.method == 'POST':
        #if request.form['ascending']:
    if ascending:
        return {'sorted' : db.all().sort()}
    #if request.form['descending']: 
    if not ascending:
        return db.all().sort(reverse= True, key=lambda x: x['volumeInfo']['publishedDate'])




"""

if __name__ == '__main__':
    app.run(debug=True)