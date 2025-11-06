# Quick Start Guide

## Setup (First Time Only)

### 1. Install Python Dependencies

```bash
cd backend
pip install flask flask-cors scikit-learn numpy
```

### 2. Start Backend Server

```bash
python app.py
```

Keep this terminal running. Server will start at `http://localhost:5000`

### 3. Open Frontend

**Option A**: Double-click `index.html`

**Option B**: Start a simple web server:
```bash
# In a new terminal, from the lMS directory
python -m http.server 8000
```

Then open: `http://localhost:8000`

## Using the Application

### Voice Commands
- Click "Voice Search" button
- Say: "Find books about programming"
- Say: "Recommend machine learning books"

### Manual Search
1. Enter interests: "artificial intelligence"
2. Add keywords: "deep learning"
3. Click "Get Recommendations"

### Browse & Filter
- Click "Browse All Books" to see entire collection
- Use search bar for specific titles/authors
- Filter by category dropdown

## Troubleshooting

**Backend not starting?**
- Make sure Python 3.8+ is installed
- Install dependencies: `pip install -r backend/requirements.txt`

**Frontend not loading?**
- Check if backend is running on port 5000
- Open browser console (F12) to see errors

**Voice not working?**
- Use Chrome, Edge, or Safari browser
- Allow microphone permissions
- Check if mic is working

## Project Structure

```
lMS/
├── backend/          # Flask server & ML engine
├── js/              # Frontend JavaScript
├── index.html       # Main page
└── README.md        # Full documentation
```

## Demo Data

System includes 25 books across categories:
- Programming, AI, Machine Learning
- Computer Science, Web Development
- Fiction, Science, Business, Self-Help

Enjoy your intelligent library assistant! 📚

