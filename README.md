# Development

```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 app.py
```

# Running

```
python3 app.py

First add some books to db from https://www.googleapis.com/books/v1/volumes:
curl -H "Content-Type: application/json" -X POST --data '{ "q": "Hobbit" }' "http://127.0.0.1:5000/db"

Return book by id:
curl "http://127.0.0.1:5000/books/QSUREAAAQBAJ"

Return books by author, and sort by published_date:
curl "http://127.0.0.1:5000/books?author=J.%20R.%20R.%20Tolkien&author=John%20Ronald%20Reuel%20Tolkien&sort=published_date"

Return books by published_date:
curl "http://127.0.0.1:5000/books?published_date=2012"
```

