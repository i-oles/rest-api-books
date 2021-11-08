import requests

res = requests.post('https://5000-violet-clam-1vvww535.ws-eu18.gitpod.io/db', json={"q":"war"})
if res.ok:
    print(res.json())

res = requests.get("https://5000-violet-clam-1vvww535.ws-eu18.gitpod.io/books?author='Rana Mitter'")
if res.ok:
    print(res.json())

res = requests.get("https://5000-violet-clam-1vvww535.ws-eu18.gitpod.io/books?date_published=2020")
if res.ok:
    print(res.json())

res = requests.get("https://5000-violet-clam-1vvww535.ws-eu18.gitpod.io/books/ckD1DwAAQBAJ")
if res.ok:
    print(res.json())


