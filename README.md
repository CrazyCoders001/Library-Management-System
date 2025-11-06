# Intelligent Book Recommendation System with Voice Assistant

A college project implementing an intelligent book recommendation system that helps library visitors find books matching their interests using AI-powered recommendations and voice assistant capabilities.

## Features

- **Intelligent Recommendations**: Content-based filtering using TF-IDF and cosine similarity
- **Voice Assistant**: Voice-enabled search and recommendations using Web Speech API
- **Advanced Search**: Filter by category, keywords, author, and title
- **Book Reader**: Read books directly in the browser with chapter navigation
- **User Feedback**: Rating system to improve future recommendations
- **Modern UI**: Beautiful, responsive interface built with Tailwind CSS
- **Real-time Results**: Fast and accurate book suggestions

## Technology Stack

### Frontend
- HTML5
- Tailwind CSS
- JavaScript (ES6+)
- Web Speech API (Voice Recognition & Synthesis)
- Font Awesome Icons

### Backend
- Python 3.8+
- Flask (Web Framework)
- SQLite (Database)
- Scikit-learn (Machine Learning)
- TF-IDF Vectorization
- Cosine Similarity Algorithm

## Project Structure

```
Library-Management-System/
├── backend/
│   ├── app.py                      # Flask server & API endpoints
│   ├── database.py                 # Database operations
│   ├── recommendation_engine.py    # ML recommendation algorithm
│   ├── requirements.txt            # Python dependencies
│   └── data/
│       └── books.db               # SQLite database (auto-generated)
├── js/
│   ├── app.js                     # Main application logic
│   └── voice.js                   # Voice assistant functionality
├── index.html                     # Main HTML page
├── start.sh                       # Automated startup script
├── README.md                      # Project documentation
├── QUICKSTART.md                  # Quick start guide
├── ARCHITECTURE.md                # System architecture details
├── TESTING_GUIDE.md               # Testing documentation
├── PRESENTATION_GUIDE.md          # Presentation guidelines
└── PROJECT_SYNOPSIS.md            # Project overview
```

## Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Modern web browser (Chrome, Firefox, Edge)

### Step 1: Install Python Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### Step 2: Start the Backend Server

```bash
python app.py
```

The server will start at `http://localhost:5000`

### Step 3: Open the Application

Open `index.html` in your web browser or use a local server:

```bash
# Option 1: Open directly
open index.html

# Option 2: Use Python's built-in server
python -m http.server 8000
```

Then navigate to `http://localhost:8000`

## Usage Guide

### 1. Get Personalized Recommendations

1. Enter your interests (e.g., "artificial intelligence, programming")
2. Add keywords (e.g., "machine learning, algorithms")
3. Click "Get Recommendations"
4. View personalized book suggestions with relevance scores

### 2. Voice Assistant

1. Click the "Voice Search" button
2. Speak your command:
   - "Find books about machine learning"
   - "Recommend programming books"
   - "Search for artificial intelligence"
3. The system will process your voice command and show results

### 3. Search & Filter

1. Use the search bar to find specific books
2. Filter by category using the dropdown
3. Browse all books in the library

### 4. View Book Details

1. Click on any book card
2. View complete information including:
   - Author, Category, Genre
   - ISBN, Summary, Keywords
   - Availability status
3. Rate the book (1-5 stars)

### 5. Read Books Online

1. Click "Read This Book" button in book details
2. Navigate through chapters using Previous/Next buttons
3. Read book content directly in your browser
4. Track your reading progress with chapter indicators

## API Endpoints

### GET /api/books
Returns all books in the library

### GET /api/categories
Returns all unique book categories

### POST /api/recommend
Request body:
```json
{
  "interests": "programming",
  "keywords": "python, algorithms",
  "limit": 10
}
```
Returns personalized book recommendations

### GET /api/search
Query parameters:
- `query`: Search term
- `category`: Filter by category

### GET /api/book/:id
Returns details of a specific book

### POST /api/feedback
Request body:
```json
{
  "book_id": 1,
  "rating": 5
}
```
Submits user feedback for a book

### GET /api/book/:id/content
Returns the readable content/chapters of a specific book

## How It Works

### Recommendation Algorithm

The system uses **Content-Based Filtering** with the following steps:

1. **Data Preprocessing**: Combines book attributes (title, author, category, keywords, summary)
2. **TF-IDF Vectorization**: Converts text data into numerical vectors
3. **Cosine Similarity**: Calculates similarity between user query and books
4. **Ranking**: Sorts books by relevance score
5. **Output**: Returns top N recommendations

### Voice Assistant

Uses the Web Speech API for:
- **Speech Recognition**: Converts voice to text
- **Command Processing**: Extracts intent and keywords
- **Speech Synthesis**: Provides audio feedback

## Sample Database

The system includes 73 pre-loaded books across categories:
- Programming & Computer Science
- Artificial Intelligence & Machine Learning
- Web Development & Data Science
- Fantasy & Science Fiction
- Mystery & Thriller
- Romance & Horror
- Literary Fiction & Dystopian
- Philosophy & Psychology
- Biography & Memoir
- Business & Economics
- Science & Popular Science
- Self-Help & Spirituality

## Future Enhancements

- Collaborative filtering using user behavior
- Deep learning models for semantic understanding
- Multi-language support
- Mobile application
- User accounts and reading history
- Book availability tracking
- Integration with library management systems

## Modules

1. **User Interface Module**: Interactive web interface
2. **Book Database Module**: SQLite database management
3. **Recommendation Engine Module**: ML-based recommendations
4. **Search & Filter Module**: Advanced search capabilities
5. **Voice Assistant Module**: Voice interaction
6. **Book Reader Module**: In-browser reading experience with chapter navigation
7. **Feedback Module**: User ratings and feedback

## Troubleshooting

### Server won't start
- Check if port 5000 is available
- Install all dependencies: `pip install -r requirements.txt`

### Voice assistant not working
- Use Chrome, Edge, or Safari (best support)
- Grant microphone permissions
- Check browser console for errors

### No recommendations showing
- Ensure backend server is running
- Check browser console for API errors
- Verify database is initialized

## Credits

**Project Type**: College Project  
**Course**: Computer Science / Information Technology  
**Topic**: Intelligent Book Recommendation System  
**Technologies**: Python, Flask, Machine Learning, JavaScript, Tailwind CSS

## License

This is an educational project for academic purposes.

## Contact

For questions or issues, please refer to your project guide or instructor.

