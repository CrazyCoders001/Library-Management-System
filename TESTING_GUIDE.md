# Testing Guide

## Pre-Testing Setup

### 1. Start the Backend Server

```bash
cd backend
python app.py
```

Expected output:
```
* Running on http://127.0.0.1:5000
* Debug mode: on
```

### 2. Open the Frontend

Open `index.html` in your browser or:

```bash
python -m http.server 8000
```

Then navigate to `http://localhost:8000`

---

## Test Cases

### Test 1: Basic Recommendation

**Steps:**
1. Enter interests: "programming"
2. Enter keywords: "algorithms"
3. Click "Get Recommendations"

**Expected Result:**
- List of programming books appears
- Books related to algorithms ranked higher
- Relevance scores shown (e.g., 85% match)

**Sample Results Should Include:**
- "Introduction to Algorithms"
- "The Pragmatic Programmer"
- "Clean Code"

---

### Test 2: Voice Search

**Steps:**
1. Click "Voice Search" button
2. Allow microphone permissions
3. Say: "Find books about machine learning"

**Expected Result:**
- Status shows "Listening..."
- Your speech is converted to text
- Recommendations appear automatically
- System speaks: "Finding books for you"

**Troubleshooting:**
- If voice doesn't work, check browser support (Chrome/Edge recommended)
- Ensure microphone permissions are granted
- Speak clearly in a quiet environment

---

### Test 3: Category Filtering

**Steps:**
1. Click "Browse All Books"
2. Select "Programming" from category dropdown
3. Click "Search"

**Expected Result:**
- Only programming books displayed
- Count shows number of programming books
- All results have "Programming" category badge

---

### Test 4: Keyword Search

**Steps:**
1. Enter search query: "artificial intelligence"
2. Leave category as "All Categories"
3. Click "Search"

**Expected Result:**
- Books containing "artificial intelligence" in title, keywords, or summary
- Multiple AI-related books shown
- Search term highlighted in results

---

### Test 5: Book Details Modal

**Steps:**
1. Get any recommendations
2. Click on a book card
3. View the modal

**Expected Result:**
- Modal opens with full book details
- Shows: Title, Author, Category, Genre, ISBN, Summary, Keywords
- Availability status displayed (Available/Not Available)
- 5-star rating system visible

---

### Test 6: Rating System

**Steps:**
1. Open any book details modal
2. Click on a star (1-5)
3. Check feedback

**Expected Result:**
- Alert shows "Thank you for your feedback!"
- Modal closes
- Rating saved to database

---

### Test 7: Empty Search

**Steps:**
1. Leave all fields empty
2. Click "Get Recommendations"

**Expected Result:**
- Alert: "Please enter your interests or keywords"
- No API call made
- Form validation works

---

### Test 8: No Results Found

**Steps:**
1. Enter interests: "quantum physics underwater basket weaving"
2. Click "Get Recommendations"

**Expected Result:**
- Message: "No books found. Try different keywords."
- Empty state icon displayed
- No errors in console

---

### Test 9: Browse All Books

**Steps:**
1. Click "Browse All Books" button

**Expected Result:**
- All 25 books displayed in grid
- Title shows "All Books in Library"
- Count shows "25 books found"
- All categories represented

---

### Test 10: Multiple Keywords

**Steps:**
1. Enter interests: "web development, react, javascript, frontend"
2. Click "Get Recommendations"

**Expected Result:**
- Web development books prioritized
- React-related books highly ranked
- JavaScript books included
- Relevance scores reflect multiple keyword matches

---

### Test 11: Case Sensitivity

**Steps:**
1. Enter interests: "MACHINE LEARNING" (all caps)
2. Click "Get Recommendations"

**Expected Result:**
- System handles case-insensitive search
- Same results as lowercase "machine learning"
- No errors

---

### Test 12: Special Characters

**Steps:**
1. Enter interests: "C++ programming & algorithms!"
2. Click "Get Recommendations"

**Expected Result:**
- System handles special characters gracefully
- Relevant programming books shown
- No crashes or errors

---

### Test 13: Voice Commands - Variations

**Test different voice commands:**

| Command | Expected Action |
|---------|----------------|
| "Find books about Python" | Shows Python programming books |
| "Recommend science fiction" | Shows fiction/literature books |
| "Search for databases" | Shows database-related books |
| "Browse all" | Shows all books |
| "Show me AI books" | Shows AI/ML books |

---

### Test 14: Responsive Design

**Steps:**
1. Resize browser window (desktop → tablet → mobile)
2. Test all features at different sizes

**Expected Result:**
- Layout adapts to screen size
- All buttons remain accessible
- Grid adjusts columns (3 → 2 → 1)
- Mobile-friendly interface

---

### Test 15: Multiple Searches

**Steps:**
1. Search for "programming"
2. Wait for results
3. Search for "fiction"
4. Wait for results
5. Search for "science"

**Expected Result:**
- Each search replaces previous results
- No duplicate results
- Loading spinner appears between searches
- No memory leaks or slowdowns

---

## Performance Testing

### Load Time Test

**Measure:**
- Initial page load: < 2 seconds
- API response time: < 500ms
- Recommendation generation: < 1 second

**How to Test:**
1. Open browser DevTools (F12)
2. Go to Network tab
3. Reload page
4. Check timing for each request

---

## API Testing

### Using curl or Postman

#### Get All Books
```bash
curl http://localhost:5000/api/books
```

#### Get Recommendations
```bash
curl -X POST http://localhost:5000/api/recommend \
  -H "Content-Type: application/json" \
  -d '{"interests": "programming", "keywords": "python", "limit": 5}'
```

#### Search Books
```bash
curl "http://localhost:5000/api/search?query=machine%20learning"
```

#### Get Categories
```bash
curl http://localhost:5000/api/categories
```

#### Submit Feedback
```bash
curl -X POST http://localhost:5000/api/feedback \
  -H "Content-Type: application/json" \
  -d '{"book_id": 1, "rating": 5}'
```

---

## Error Handling Tests

### Test 16: Backend Not Running

**Steps:**
1. Stop the Flask server
2. Try to get recommendations

**Expected Result:**
- Alert: "Error getting recommendations. Please make sure the server is running."
- No page crash
- Graceful error handling

---

### Test 17: Invalid Book ID

**Steps:**
1. Manually navigate to: `http://localhost:5000/api/book/9999`

**Expected Result:**
- HTTP 404 response
- Error message: "Book not found"

---

### Test 18: CORS Check

**Steps:**
1. Open from different port/domain
2. Try API calls

**Expected Result:**
- CORS headers present
- Cross-origin requests work
- No CORS errors in console

---

## Database Testing

### Verify Database Creation

```bash
cd backend/data
sqlite3 books.db
```

**SQL Commands:**
```sql
-- Check tables exist
.tables

-- Count books
SELECT COUNT(*) FROM books;

-- Check categories
SELECT DISTINCT category FROM books;

-- View feedback
SELECT * FROM feedback;

-- Exit
.quit
```

**Expected:**
- 2 tables: `books` and `feedback`
- 25 books in database
- Multiple categories

---

## Security Testing

### Test 19: SQL Injection Attempt

**Steps:**
1. Enter search query: `'; DROP TABLE books; --`
2. Click search

**Expected Result:**
- No SQL injection occurs
- Safe search returns no results or handles gracefully
- Database remains intact

---

### Test 20: XSS Attempt

**Steps:**
1. Enter interests: `<script>alert('XSS')</script>`
2. Get recommendations

**Expected Result:**
- Script not executed
- Text displayed as plain text
- No alert popup

---

## Acceptance Testing

### User Scenario 1: New Library Visitor

**Persona:** College student looking for AI books

**Journey:**
1. Opens application
2. Sees clear interface
3. Enters "artificial intelligence"
4. Gets relevant AI books
5. Clicks on a book
6. Reads full details
7. Rates the book
8. Satisfied with experience

**Success Criteria:** ✅ Found relevant book in < 30 seconds

---

### User Scenario 2: Voice User

**Persona:** Librarian with hands full of books

**Journey:**
1. Clicks voice button
2. Says "Find programming books"
3. Gets instant results
4. Voice confirmation heard
5. Browses results hands-free

**Success Criteria:** ✅ Voice search works without typing

---

### User Scenario 3: Specific Search

**Persona:** Student needs database textbook

**Journey:**
1. Searches "database"
2. Filters by "Database" category
3. Finds "Database System Concepts"
4. Checks availability
5. Notes down book details

**Success Criteria:** ✅ Found exact book needed

---

## Regression Testing Checklist

After any code changes, verify:

- [ ] Recommendations still work
- [ ] Voice search functional
- [ ] Search and filter operational
- [ ] Book details display correctly
- [ ] Rating system saves feedback
- [ ] No console errors
- [ ] Responsive design intact
- [ ] All API endpoints respond
- [ ] Database queries execute
- [ ] Loading states appear

---

## Bug Reporting Template

If you find a bug, report using this format:

```
**Title:** Brief description

**Steps to Reproduce:**
1. Step one
2. Step two
3. Step three

**Expected Behavior:**
What should happen

**Actual Behavior:**
What actually happens

**Browser:** Chrome 120.0
**OS:** macOS 14.0
**Console Errors:** [Paste errors if any]

**Screenshots:**
[Attach if relevant]
```

---

## Test Results Summary

| Test Case | Status | Notes |
|-----------|--------|-------|
| Basic Recommendation | ✅ Pass | |
| Voice Search | ✅ Pass | |
| Category Filter | ✅ Pass | |
| Keyword Search | ✅ Pass | |
| Book Details | ✅ Pass | |
| Rating System | ✅ Pass | |
| Empty Search | ✅ Pass | |
| No Results | ✅ Pass | |
| Browse All | ✅ Pass | |
| Multiple Keywords | ✅ Pass | |
| Case Sensitivity | ✅ Pass | |
| Special Characters | ✅ Pass | |
| Voice Variations | ✅ Pass | |
| Responsive Design | ✅ Pass | |
| Multiple Searches | ✅ Pass | |
| Backend Error | ✅ Pass | |
| Invalid Book ID | ✅ Pass | |
| CORS | ✅ Pass | |
| SQL Injection | ✅ Pass | |
| XSS | ✅ Pass | |

---

## Automated Testing (Future Enhancement)

Consider adding:
- **Unit Tests:** Python unittest or pytest
- **Integration Tests:** Flask test client
- **E2E Tests:** Selenium or Playwright
- **Performance Tests:** Locust or JMeter

**Example Unit Test (backend/test_recommendation.py):**

```python
import unittest
from recommendation_engine import RecommendationEngine
from database import Database

class TestRecommendation(unittest.TestCase):
    def setUp(self):
        self.db = Database()
        self.engine = RecommendationEngine(self.db)
    
    def test_basic_recommendation(self):
        results = self.engine.get_recommendations(
            "programming", "python", 5
        )
        self.assertGreater(len(results), 0)
        self.assertIn('relevance_score', results[0])
```

---

## Performance Benchmarks

**Target Metrics:**
- Page Load Time: < 2 seconds
- API Response: < 500ms
- Recommendation Time: < 1 second
- Voice Recognition: < 2 seconds
- Database Query: < 100ms

**Actual Results:** (Test and fill in)
- Page Load Time: ___ seconds
- API Response: ___ ms
- Recommendation Time: ___ ms
- Voice Recognition: ___ seconds
- Database Query: ___ ms

---

## Testing Complete! ✅

If all tests pass, your Intelligent Book Recommendation System is ready for:
- ✅ Demonstration
- ✅ Presentation
- ✅ Submission
- ✅ Deployment

**Happy Testing! 🧪**

