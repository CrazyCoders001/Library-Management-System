from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class RecommendationEngine:
    def __init__(self, database):
        self.db = database
        self.vectorizer = TfidfVectorizer(stop_words='english')
    
    def get_recommendations(self, interests, keywords, limit=10):
        books = self.db.get_all_books()
        
        if not books:
            return []
        
        user_query = f"{interests} {keywords}".strip()
        
        if not user_query:
            return books[:limit]
        
        book_texts = []
        for book in books:
            text = f"{book['title']} {book['author']} {book['category']} {book['genre']} {book['keywords']} {book['summary']}"
            book_texts.append(text)
        
        all_texts = [user_query] + book_texts
        
        try:
            tfidf_matrix = self.vectorizer.fit_transform(all_texts)
            user_vector = tfidf_matrix[0:1]
            book_vectors = tfidf_matrix[1:]
            
            similarities = cosine_similarity(user_vector, book_vectors)[0]
            
            book_scores = list(zip(books, similarities))
            book_scores.sort(key=lambda x: x[1], reverse=True)
            
            recommendations = []
            for book, score in book_scores[:limit]:
                book_copy = book.copy()
                book_copy['relevance_score'] = float(score)
                recommendations.append(book_copy)
            
            return recommendations
        
        except Exception as e:
            print(f"Error in recommendation: {e}")
            return books[:limit]

