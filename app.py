from flask import Flask, abort, render_template
from tinydb import TinyDB, Query
from collections import OrderedDict
import requests

# Todo:
# 1. change source url in post_book
# 2. redirect,
# 3. q= war
# 4. author & author
# 5. filter with sort together
# 6. spliting authors, error? J.R.R Tolkien
# 7. what if type two names of author Ronadl Raul Tolkien
# 8. books list - only title?


app = Flask(__name__)
db = TinyDB('db.json')

base_url = 'https://www.googleapis.com/books/v1/volumes?q=Hobbit'
data = requests.get(base_url).json()
items = data['items']


@app.route("/")
def home():
    return render_template('app/index.html')


@app.route('/books')
def get_all_books():
    return {'all books' : db.all()}


@app.route('/books/date', methods=['POST', 'GET'])
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


@app.route('/books/authors', methods=['POST', 'GET'])
def filter_by_authors():
    
    filtered_books = []

    def find_book_by_author(name):
        for book in db.all():
            author = book['volumeInfo']['authors']
            if name in author:
                filtered_books.append(book)

    #if request.method == 'POST':
        #authors = request.form['autors'].replace(',' , '')
    authors = 'tolkien, fisher'
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


def return_key_if_exist(book, key):
    try:
        return book['volumeInfo'][key]
    except:
        return None
    

@app.route('/books/<bookId>')
def get_book(bookId):
    b = Query()
    if db.contains(b.id == bookId):
        book = db.get(b.id == bookId)
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


def all_keys_in_book(book):
    book = OrderedDict(book)
    keys = book.keys()
    values = book.values()
    all_fields = dict(zip(keys, values))
    return all_fields


@app.route('/books/posted')
def send_book():
    b = Query()
    for book in items:
        if db.contains(b.id == book['id']):
            db.upsert(all_keys_in_book(book), b.id == book['id'])
        else:
            db.insert(all_keys_in_book(book))

    return {'all books' : db.all()}


if __name__ == '__main__':
    app.run(debug=True)