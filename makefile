run:
	python3 app.py

format:
	ruff check . --fix
	ruff format .