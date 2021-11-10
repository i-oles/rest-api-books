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

curl -H "Content-Type: application/json" -X POST --data '{ "q": "Hobbit" }' "http://localhost:5000/db"

curl "http://localhost:5000/books/IbbEuQYtTrQC"

curl "http://localhost:5000/books?author=J.%20R.%20R.%20Tolkien&author=John%20Ronald%20Reuel%20Tolkien&sort=published_date"

curl "http://localhost:5000/books?published_date=2012"

```

# Running on Pythonanywhere.com

```
python3 app.py

curl -H "Content-Type: application/json" -X POST --data '{ "q": "Hobbit" }' "http://igoroles.pythonanywhere.com/db"

curl "http://igoroles.pythonanywhere.com/books/IbbEuQYtTrQC"

curl "http://igoroles.pythonanywhere.com/books?author=J.%20R.%20R.%20Tolkien&author=John%20Ronald%20Reuel%20Tolkien&sort=published_date"

curl "http://igoroles.pythonanywhere.com/books?published_date=2012"

```

