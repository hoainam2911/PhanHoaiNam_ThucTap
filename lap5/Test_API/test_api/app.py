from flask import Flask, jsonify, request
from models import db, Book

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/books', methods=['POST'])
def add_book():
    data = request.get_json()
    if not all(k in data for k in ("title", "author", "published_year")):
        return jsonify({'message': 'Missing required fields'}), 400

    try:
        published_year = int(data['published_year'])
        if not (1000 <= published_year <= 9999):
            raise ValueError
    except (ValueError, TypeError):
        return jsonify({'message': 'Invalid publication year'}), 400

    new_book = Book(title=data['title'], author=data['author'], published_year=published_year)
    db.session.add(new_book)
    db.session.commit()
    return jsonify({'message': 'Book added successfully!'}), 201

@app.route('/books', methods=['GET'])
def get_books():
    books = Book.query.all()
    books_list = [{'id': book.id, 'title': book.title, 'author': book.author, 'published_year': book.published_year} for book in books]
    return jsonify(books_list)

@app.route('/books/<int:id>', methods=['PUT'])
def update_book(id):
    book = Book.query.get(id)
    if not book:
        return jsonify({'message': 'Book not found!'}), 404

    data = request.get_json()
    if 'title' in data and data['title'] is not None:
        book.title = data['title']
    if 'author' in data and data['author'] is not None:
        book.author = data['author']
    if 'published_year' in data and data['published_year'] is not None:
        try:
            published_year = int(data['published_year'])
            if not (1000 <= published_year <= 9999):
                raise ValueError
            book.published_year = published_year
        except (ValueError, TypeError):
            return jsonify({'message': 'Invalid publication year'}), 400

    db.session.commit()
    return jsonify({'message': 'Book updated successfully!'})

@app.route('/books/<int:id>', methods=['DELETE'])
def delete_book(id):
    book = Book.query.get(id)
    if not book:
        return jsonify({'message': 'Book not found!'}), 404

    db.session.delete(book)
    db.session.commit()
    return jsonify({'message': 'Book deleted successfully!'})

if __name__ == '__main__':
    app.run(debug=True)
