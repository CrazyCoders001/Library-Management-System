# Setup Guide - Library Management System

Complete step-by-step guide to run this project on a new laptop.

---

## Prerequisites

Before you begin, ensure you have the following installed:

1. **Python 3.8 or higher**
   ```bash
   python3 --version
   ```
   If not installed, download from: https://www.python.org/downloads/

2. **Git**
   ```bash
   git --version
   ```
   If not installed, download from: https://git-scm.com/downloads

3. **Modern Web Browser**
   - Chrome, Firefox, Edge, or Safari

---

## Step 1: Clone the Repository

Open your terminal and run:

```bash
# Clone the repository
git clone git@github-second:CrazyCoders001/Library-Management-System.git

# Navigate to the project directory
cd Library-Management-System
```

**Alternative (if using HTTPS):**
```bash
git clone https://github.com/CrazyCoders001/Library-Management-System.git
cd Library-Management-System
```

---

## Step 2: Set Up the Backend

### Option A: Automated Setup (Recommended)

```bash
# Make the startup script executable
chmod +x start.sh

# Run the startup script
./start.sh
```

The script will automatically:
- Create a virtual environment
- Install all dependencies
- Start the Flask server

### Option B: Manual Setup

```bash
# Navigate to backend directory
cd backend

# Create a virtual environment (optional but recommended)
python3 -m venv venv

# Activate the virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start the Flask server
python app.py
```

---

## Step 3: Verify Backend is Running

You should see output like:
```
* Running on http://127.0.0.1:5000
* Running on http://localhost:5000
```

**Test the API:**
Open a new terminal and run:
```bash
curl http://localhost:5000/
```

You should see a JSON response with API endpoints.

---

## Step 4: Open the Frontend

### Option 1: Direct File Opening (Quick Start)

Simply open `index.html` in your web browser:

**macOS:**
```bash
open index.html
```

**Linux:**
```bash
xdg-open index.html
```

**Windows:**
```bash
start index.html
```

Or manually: Right-click `index.html` → Open With → Your Browser

### Option 2: Using Python HTTP Server (Recommended)

Open a **new terminal** (keep the backend running):

```bash
# Navigate to project root
cd Library-Management-System

# Start a simple HTTP server
python3 -m http.server 8000
```

Then open your browser and visit:
```
http://localhost:8000
```

---

## Step 5: Using the Website

### 1. Get Recommendations

1. Enter your interests (e.g., "programming, AI, machine learning")
2. Add keywords (e.g., "python, algorithms, data science")
3. Click **"Get Recommendations"**
4. View personalized book suggestions with relevance scores

### 2. Browse All Books

- Click **"Browse All Books"** to see the entire library (72 books)

### 3. Search Books

1. Use the search bar to find books by title, author, or keywords
2. Filter by category using the dropdown menu
3. Click **"Search"**

### 4. Voice Search

1. Click the **"Voice Search"** button in the navigation bar
2. Grant microphone permissions if prompted
3. Speak your query (e.g., "Find books about machine learning")
4. View results based on your voice command

### 5. View Book Details

1. Click on any book card
2. View complete information:
   - Author, Category, Genre
   - ISBN, Summary, Keywords
   - Availability status
3. Rate the book (1-5 stars)

### 6. Read Books Online

1. In the book details modal, click **"Read This Book"**
2. Read the book content in a beautiful reader interface
3. Navigate chapters using **Previous/Next** buttons
4. Close the reader when finished

---

## Troubleshooting

### Backend Server Won't Start

**Problem:** Port 5000 is already in use

**Solution:**
```bash
# Find and kill process using port 5000
# macOS/Linux:
lsof -ti:5000 | xargs kill -9

# Windows:
netstat -ano | findstr :5000
taskkill /PID <PID_NUMBER> /F
```

### Dependencies Installation Fails

**Problem:** pip install errors

**Solution:**
```bash
# Upgrade pip first
pip install --upgrade pip

# Try installing again
pip install -r backend/requirements.txt
```

### Voice Assistant Not Working

**Problem:** Voice search button doesn't respond

**Solutions:**
- Use Chrome, Edge, or Safari (best browser support)
- Grant microphone permissions when prompted
- Check browser console (F12) for errors
- Ensure you're using HTTPS or localhost

### No Books Showing

**Problem:** Empty book grid or no recommendations

**Solutions:**
1. Verify backend server is running (`http://localhost:5000`)
2. Check browser console (F12) for API errors
3. Ensure database exists (`backend/data/books.db`)
4. If database is corrupted, delete it and restart server:
   ```bash
   rm backend/data/books.db
   python backend/app.py
   ```

### CORS Errors

**Problem:** Browser shows CORS policy errors

**Solution:**
- Ensure backend server is running
- Use `python -m http.server` instead of opening file directly
- Check that flask-cors is installed:
  ```bash
  pip install flask-cors
  ```

---

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
└── README.md                      # Project documentation
```

---

## Quick Commands Reference

```bash
# Start backend server
cd backend && python app.py

# Start frontend server
python3 -m http.server 8000

# Stop backend server
Ctrl + C

# Reinstall dependencies
cd backend && pip install -r requirements.txt

# Delete and recreate database
rm backend/data/books.db && python backend/app.py
```

---

## System Requirements

- **OS**: macOS, Linux, or Windows
- **Python**: 3.8 or higher
- **RAM**: 2GB minimum, 4GB recommended
- **Storage**: 500MB for dependencies and database
- **Browser**: Chrome 90+, Firefox 88+, Safari 14+, Edge 90+

---

## Features Overview

✅ **72 Books** across diverse genres
✅ **AI-Powered Recommendations** using TF-IDF and cosine similarity
✅ **Voice Assistant** with Web Speech API
✅ **Book Reader** with chapter navigation
✅ **Advanced Search** with filters
✅ **Rating System** for user feedback
✅ **Fully Responsive** design for all devices

---

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review `README.md` for detailed documentation
3. Check `TESTING_GUIDE.md` for testing procedures
4. Consult your project guide or instructor

---

## License

This is an educational project for academic purposes.

---

**Last Updated:** November 6, 2025
**Version:** 1.0

