# About
```
This project is a simple REST API built with Flask
that interacts with the Google Books API to fetch
and store book data in a local database.
Users can retrieve all books, retrieve book by ID,
filter results by author or publication date and sort the output.
```

# Development

```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 app.py
```

# Running

`python3 app.py`

First add some books to db from https://www.googleapis.com/books/v1/volumes:  
`curl -H "Content-Type: application/json" -X POST --data '{ "q": "Hobbit" }' "http://127.0.0.1:5000/db"`

Return book by id (replace 'some_id' with id from db.json file):
`curl "http://127.0.0.1:5000/books/some_id"`

Return books by author, and sort by published_date:  
`curl "http://127.0.0.1:5000/books?author=J.%20R.%20R.%20Tolkien&author=John%20Ronald%20Reuel%20Tolkien&sort=published_date"`

Return books by published_date:  
`curl "http://127.0.0.1:5000/books?published_date=2012"`

