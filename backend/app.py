from flask import Flask, request, jsonify
from flask_cors import CORS
from database import Database
from recommendation_engine import RecommendationEngine

app = Flask(__name__)
CORS(app)

db = Database()
recommender = RecommendationEngine(db)

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        'message': 'Library Management System API',
        'status': 'Running',
        'endpoints': {
            'GET /api/books': 'Get all books',
            'GET /api/categories': 'Get all categories',
            'POST /api/recommend': 'Get book recommendations',
            'GET /api/search': 'Search books',
            'GET /api/book/<id>': 'Get book details',
            'GET /api/book/<id>/content': 'Get book content/chapters',
            'POST /api/feedback': 'Submit feedback'
        },
        'frontend': 'Open index.html in your browser'
    })

@app.route('/api/books', methods=['GET'])
def get_books():
    books = db.get_all_books()
    return jsonify(books)

@app.route('/api/categories', methods=['GET'])
def get_categories():
    categories = db.get_categories()
    return jsonify(categories)

@app.route('/api/recommend', methods=['POST'])
def recommend():
    data = request.json
    interests = data.get('interests', '')
    keywords = data.get('keywords', '')
    limit = data.get('limit', 10)
    
    recommendations = recommender.get_recommendations(interests, keywords, limit)
    return jsonify(recommendations)

@app.route('/api/search', methods=['GET'])
def search_books():
    query = request.args.get('query', '')
    category = request.args.get('category', '')
    
    books = db.search_books(query, category)
    return jsonify(books)

@app.route('/api/book/<int:book_id>', methods=['GET'])
def get_book(book_id):
    book = db.get_book_by_id(book_id)
    if book:
        return jsonify(book)
    return jsonify({'error': 'Book not found'}), 404

@app.route('/api/feedback', methods=['POST'])
def submit_feedback():
    data = request.json
    book_id = data.get('book_id')
    rating = data.get('rating')
    
    db.add_feedback(book_id, rating)
    return jsonify({'message': 'Feedback submitted successfully'})

@app.route('/api/book/<int:book_id>/content', methods=['GET'])
def get_book_content(book_id):
    content = db.get_book_content(book_id)
    if content:
        return jsonify(content)
    return jsonify({'message': 'No content available for this book'}), 404

if __name__ == '__main__':
    app.run(debug=True, port=5000)

