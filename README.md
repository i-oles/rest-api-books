# Development

```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 app.py
```

# Running

```
python app.py

curl -H "Content-Type: application/json" -X POST --data '{ "q": "Hobbit" }' "http://localhost:5000/db"

curl "http://localhost:5000/books/rToaogEACAAJ"

curl  "http://localhost:5000/books?author=J.%20R.%20R.%20Tolkien&author=John%20Ronald%20Reuel%20Tolkien&sort=published_date"

curl "http://localhost:5000/books?published_date=2012"

```
