"""




base = {
    'book-id-1': {
        'name': 'Hobbit'
    },
    'book-id-2': {
        'name': '50 shades of grey'
    }
}



@app.errorhandler(404)
def not_found(error):
   return { 'error': 'Not found' }, 404



"""