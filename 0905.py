from flask import Flask
from flask_restx import Api, Resource, fields

app = Flask(__name__)
api = Api(app, version='1.0', title='Sample API', description='A simple API')

# Define a namespace
ns = api.namespace('books', description='Book operations')

book_model = api.model('Book', {
    'id': fields.Integer(required=True, description='The book identifier'),
    'title': fields.String(required=True, description='The book title'),
    'author': fields.String(required=True, description='The book author')
})
books = [
    {"id": 1, "title": "1984", "author": "George Orwell"},
    {"id": 2, "title": "Brave New World", "author": "Aldous Huxley"}
]

@ns.route('/')
class BookList(Resource):
    @ns.doc('list_books')
    @ns.marshal_list_with(book_model)
    def get(self):
        """List all books"""
        return books

    @ns.doc('create_book')
    @ns.expect(book_model)
    @ns.marshal_with(book_model, code=201)
    def post(self):
        """Create a new book"""
        new_book = api.payload
        books.append(new_book)
        return new_book, 201

@ns.route('/<int:id>')
class Book(Resource):
    def get(self, id):
        """Fetch a book given its identifier"""
        book = next((b for b in books if b['id'] == id), None)
        if book:
            return book
        api.abort(404, "Book {} doesn't exist".format(id))

    @ns.doc('update_book')
    @ns.expect(book_model)
    @ns.marshal_with(book_model, code=404)
    def put(self, id):
        """Update a book given its identifier"""
        book = next((b for b in books if b['id'] == id), None)
        if book:
            data = api.payload
            book.update(data)
            return book
        api.abort(404, "Book {} doesn't exist".format(id))

    def delete(self, id):
        """Delete a book given its identifier"""
        global books
        books = [b for b in books if b['id'] != id]
        return '', 204

# Add the namespace to the API
api.add_namespace(ns)

if __name__ == '__main__':
    app.run(debug=True)

# books = [
#     {"id": 1, "title": "1984", "author": "George Orwell"},
#     {"id": 2, "title": "Brave New World", "author": "Aldous Huxley"}
# ]
#
# @app.route('/')
# def home():
#     return "Welcome to the Book API!"
#
# @app.route('/books', methods=['GET'])
# def get_books():
#     return jsonify(books)
#
# @app.route('/books', methods=['POST'])
# def add_book():
#     new_book = request.get_json()
#     books.append(new_book)
#     return jsonify(new_book), 201 # 201 생성됨 상태 코드 반환
#
# @app.route('/books/<int:id>', methods=['PUT'])
# def update_book(id):
#     book = next((b for b in books if b['id'] == id), None)
#
#     if book:
#         data = request.get_json()
#         book.update(data)
#         return jsonify(book)
#     return jsonify({'error': 'Book not found'}), 404
#
# @app.route('/books/<int:id>', methods=['DELETE'])
# def delete_book(id):
#     global books
#     books = [b for b in books if b['id'] != id]
#     return '', 204
#
# if __name__ == '__main__':
#     app.run(debug=True)