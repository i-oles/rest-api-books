from flask import Flask, abort

app = Flask(__name__)

db = {
    'book-id-1': {
        'name': 'Hobbit'
    },
    'book-id-2': {
        'name': '50 shades of grey'
    }
}

@app.route("/")
def home():
    return "<p>Hello, World!</p>"

@app.errorhandler(404)
def not_found(error):
   return { 'error': 'Not found' }, 404

@app.route('/books')
@app.route('/books/<bookId>')
def get_books(**kwargs):
    bookId = kwargs.get('bookId')
    
    if bookId:
        return db.get(bookId, None) or abort(404)
    else:
        return {
            'books': list(db.values())
        }

if __name__ == '__main__':
    app.run(debug=True)