books = [{'book1': 'a'}, {'book2': 'b'}]

x = sorted(books, key=lambda book: book['book1'])

print(x)
