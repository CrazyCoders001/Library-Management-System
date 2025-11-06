# System Architecture

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                       USER INTERFACE                         │
│  (HTML + Tailwind CSS + JavaScript + Voice Assistant)       │
└────────────────────┬────────────────────────────────────────┘
                     │
                     │ HTTP/REST API
                     │
┌────────────────────▼────────────────────────────────────────┐
│                    FLASK BACKEND SERVER                      │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              API ENDPOINTS                            │  │
│  │  /api/books, /api/recommend, /api/search            │  │
│  │  /api/categories, /api/feedback                      │  │
│  └──────────────────┬───────────────────────────────────┘  │
│                     │                                        │
│  ┌──────────────────▼───────────────────────────────────┐  │
│  │        RECOMMENDATION ENGINE                          │  │
│  │  - TF-IDF Vectorization                              │  │
│  │  - Cosine Similarity Calculation                     │  │
│  │  - Content-Based Filtering                           │  │
│  │  - Ranking & Scoring                                 │  │
│  └──────────────────┬───────────────────────────────────┘  │
│                     │                                        │
│  ┌──────────────────▼───────────────────────────────────┐  │
│  │           DATABASE MODULE                             │  │
│  │  - Book CRUD Operations                              │  │
│  │  - Search & Filter Logic                             │  │
│  │  - Feedback Storage                                   │  │
│  └──────────────────┬───────────────────────────────────┘  │
└────────────────────┼────────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────────┐
│                    SQLite DATABASE                           │
│  ┌──────────────────┐      ┌──────────────────────┐        │
│  │   Books Table    │      │  Feedback Table      │        │
│  │  - id            │      │  - id                │        │
│  │  - title         │      │  - book_id           │        │
│  │  - author        │      │  - rating            │        │
│  │  - category      │      │  - timestamp         │        │
│  │  - genre         │      └──────────────────────┘        │
│  │  - keywords      │                                       │
│  │  - summary       │                                       │
│  │  - isbn          │                                       │
│  │  - available     │                                       │
│  └──────────────────┘                                       │
└─────────────────────────────────────────────────────────────┘
```

## Data Flow Diagram

### Recommendation Flow

```
User Input
   │
   ├─── Text Input (Interests/Keywords)
   │       │
   │       ▼
   │   Frontend Validation
   │       │
   │       ▼
   │   POST /api/recommend
   │       │
   │       ▼
   ├─── Voice Input ───────► Speech Recognition
           │                       │
           ▼                       ▼
      Extract Intent          Convert to Text
           │                       │
           └───────────┬───────────┘
                       │
                       ▼
              Backend Processing
                       │
         ┌─────────────┼─────────────┐
         │             │             │
         ▼             ▼             ▼
    Fetch Books   Preprocess    Create Vectors
                     Data
         │             │             │
         └─────────────┼─────────────┘
                       │
                       ▼
            Calculate Similarity
                       │
                       ▼
              Rank by Score
                       │
                       ▼
            Return Top Results
                       │
                       ▼
             Display to User
```

## Component Breakdown

### 1. Frontend Components

#### index.html
- Main structure
- Navigation bar
- Search forms
- Results display area
- Modal for book details

#### app.js
- API communication
- User interactions
- Dynamic content rendering
- Search and filter logic
- Feedback submission

#### voice.js
- Speech recognition
- Voice command processing
- Text-to-speech feedback
- Command parsing

### 2. Backend Components

#### app.py (Flask Server)
```python
Routes:
- GET  /api/books         → List all books
- GET  /api/categories    → List categories
- POST /api/recommend     → Get recommendations
- GET  /api/search        → Search books
- GET  /api/book/:id      → Get book details
- POST /api/feedback      → Submit rating
```

#### database.py
```python
Functions:
- init_database()         → Create tables
- populate_sample_data()  → Add books
- get_all_books()        → Fetch books
- search_books()         → Filter books
- add_feedback()         → Store ratings
```

#### recommendation_engine.py
```python
Algorithm:
1. Combine book attributes into text
2. Apply TF-IDF vectorization
3. Calculate cosine similarity
4. Rank by relevance score
5. Return top N matches
```

## Technology Stack Details

### Frontend Technologies

| Technology | Purpose |
|------------|---------|
| HTML5 | Structure and layout |
| Tailwind CSS | Styling and responsive design |
| JavaScript ES6+ | Application logic |
| Web Speech API | Voice recognition |
| Font Awesome | Icons |
| Fetch API | HTTP requests |

### Backend Technologies

| Technology | Purpose |
|------------|---------|
| Python 3.8+ | Programming language |
| Flask | Web framework |
| Flask-CORS | Cross-origin requests |
| SQLite3 | Database |
| Scikit-learn | Machine learning |
| NumPy | Numerical operations |

## Machine Learning Pipeline

```
┌─────────────────────────────────────────────────────────┐
│                INPUT: User Query                         │
│            "machine learning algorithms"                 │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│              PREPROCESSING                               │
│  - Lowercase conversion                                  │
│  - Tokenization                                          │
│  - Stop word handling (by TF-IDF)                       │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│           TF-IDF VECTORIZATION                          │
│  - Term Frequency calculation                            │
│  - Inverse Document Frequency                            │
│  - Feature vector creation                               │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│           COSINE SIMILARITY                             │
│  similarity = (A · B) / (||A|| × ||B||)                │
│  where A = user vector, B = book vector                 │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│               RANKING                                    │
│  Sort books by similarity score (0-1)                    │
│  Higher score = more relevant                            │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│             OUTPUT: Ranked Books                         │
│  1. Deep Learning (95% match)                           │
│  2. Artificial Intelligence (87% match)                  │
│  3. Machine Learning Algorithms (82% match)              │
└─────────────────────────────────────────────────────────┘
```

## Security Considerations

1. **CORS**: Configured to allow frontend-backend communication
2. **Input Validation**: All user inputs are sanitized
3. **SQL Injection Prevention**: Using parameterized queries
4. **XSS Protection**: Proper HTML escaping in frontend

## Scalability

### Current Implementation
- SQLite database (suitable for college project)
- In-memory ML model
- Single-threaded Flask server

### Production Enhancements
- PostgreSQL/MySQL for multi-user support
- Redis for caching recommendations
- Gunicorn/uWSGI for production deployment
- Docker containerization
- Load balancing
- CDN for static assets

## Performance Optimization

1. **Database Indexing**: On category, title, author fields
2. **Lazy Loading**: Books loaded on demand
3. **Caching**: TF-IDF model cached in memory
4. **Pagination**: Limit results per query

## Error Handling

```
Frontend → Backend
    │          │
    │          ├─ Try-Catch blocks
    │          ├─ HTTP status codes
    │          └─ Error messages
    │
    └─ Display user-friendly errors
```

## Deployment Architecture

```
Development:
  Frontend: File System (index.html)
  Backend: Flask Development Server (port 5000)
  Database: SQLite file

Production (Recommended):
  Frontend: Nginx/Apache static hosting
  Backend: Gunicorn + Flask
  Database: PostgreSQL/MySQL
  Proxy: Nginx reverse proxy
  HTTPS: SSL/TLS certificates
```

This architecture ensures modularity, maintainability, and scalability for future enhancements.

