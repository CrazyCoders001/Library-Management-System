const API_URL = 'http://localhost:5000/api';

let currentBooks = [];
let currentBookData = null;
let currentChapters = [];
let currentChapterIndex = 0;

document.addEventListener('DOMContentLoaded', function() {
    loadCategories();
    setupEventListeners();
});

function setupEventListeners() {
    document.getElementById('recommendBtn').addEventListener('click', getRecommendations);
    document.getElementById('browseBtn').addEventListener('click', browseAllBooks);
    document.getElementById('searchBtn').addEventListener('click', searchBooks);
    document.getElementById('closeModal').addEventListener('click', closeModal);
    document.getElementById('closeReader').addEventListener('click', closeReader);
    document.getElementById('prevChapter').addEventListener('click', previousChapter);
    document.getElementById('nextChapter').addEventListener('click', nextChapter);
    
    document.getElementById('interests').addEventListener('keypress', function(e) {
        if (e.key === 'Enter') getRecommendations();
    });
    
    document.getElementById('searchQuery').addEventListener('keypress', function(e) {
        if (e.key === 'Enter') searchBooks();
    });
}

async function loadCategories() {
    try {
        const response = await fetch(`${API_URL}/categories`);
        const categories = await response.json();
        
        const select = document.getElementById('categoryFilter');
        categories.forEach(category => {
            const option = document.createElement('option');
            option.value = category;
            option.textContent = category;
            select.appendChild(option);
        });
    } catch (error) {
        console.error('Error loading categories:', error);
    }
}

async function getRecommendations() {
    const interests = document.getElementById('interests').value.trim();
    const keywords = document.getElementById('keywords').value.trim();
    
    if (!interests && !keywords) {
        alert('Please enter your interests or keywords');
        return;
    }
    
    showLoading(true);
    
    try {
        const response = await fetch(`${API_URL}/recommend`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ interests, keywords, limit: 12 })
        });
        
        const books = await response.json();
        currentBooks = books;
        displayBooks(books, 'Recommended Books for You');
    } catch (error) {
        console.error('Error getting recommendations:', error);
        alert('Error getting recommendations. Please make sure the server is running.');
    } finally {
        showLoading(false);
    }
}

async function browseAllBooks() {
    showLoading(true);
    
    try {
        const response = await fetch(`${API_URL}/books`);
        const books = await response.json();
        currentBooks = books;
        displayBooks(books, 'All Books in Library');
    } catch (error) {
        console.error('Error browsing books:', error);
        alert('Error loading books. Please make sure the server is running.');
    } finally {
        showLoading(false);
    }
}

async function searchBooks() {
    const query = document.getElementById('searchQuery').value.trim();
    const category = document.getElementById('categoryFilter').value;
    
    showLoading(true);
    
    try {
        const params = new URLSearchParams();
        if (query) params.append('query', query);
        if (category) params.append('category', category);
        
        const response = await fetch(`${API_URL}/search?${params}`);
        const books = await response.json();
        currentBooks = books;
        
        const title = query ? `Search Results for "${query}"` : `Books in ${category}`;
        displayBooks(books, title);
    } catch (error) {
        console.error('Error searching books:', error);
        alert('Error searching books. Please make sure the server is running.');
    } finally {
        showLoading(false);
    }
}

function displayBooks(books, title) {
    const resultsSection = document.getElementById('resultsSection');
    const bookGrid = document.getElementById('bookGrid');
    const resultsTitle = document.getElementById('resultsTitle');
    const resultsCount = document.getElementById('resultsCount');
    
    resultsTitle.textContent = title;
    resultsCount.textContent = `${books.length} book${books.length !== 1 ? 's' : ''} found`;
    
    bookGrid.innerHTML = '';
    
    if (books.length === 0) {
        bookGrid.innerHTML = `
            <div class="col-span-full text-center py-12">
                <i class="fas fa-book-open text-6xl text-gray-300 mb-4"></i>
                <p class="text-gray-600 text-lg">No books found. Try different keywords.</p>
            </div>
        `;
    } else {
        books.forEach(book => {
            const bookCard = createBookCard(book);
            bookGrid.appendChild(bookCard);
        });
    }
    
    resultsSection.classList.remove('hidden');
}

function createBookCard(book) {
    const card = document.createElement('div');
    card.className = 'bg-white rounded-lg shadow-md hover:shadow-xl transition p-4 sm:p-6 cursor-pointer touch-manipulation';
    
    const relevanceScore = book.relevance_score ? Math.round(book.relevance_score * 100) : null;
    
    card.innerHTML = `
        <div class="flex justify-between items-start mb-3 gap-2">
            <div class="bg-indigo-100 text-indigo-800 px-2 sm:px-3 py-1 rounded-full text-xs sm:text-sm font-semibold truncate">
                ${book.category}
            </div>
            ${relevanceScore ? `
                <div class="bg-green-100 text-green-800 px-2 py-1 rounded text-xs font-semibold whitespace-nowrap">
                    ${relevanceScore}% Match
                </div>
            ` : ''}
        </div>
        <h3 class="text-lg sm:text-xl font-bold text-gray-800 mb-2 line-clamp-2">${book.title}</h3>
        <p class="text-sm sm:text-base text-gray-600 mb-2"><i class="fas fa-user mr-2"></i>${book.author}</p>
        <p class="text-gray-500 text-xs sm:text-sm mb-3 line-clamp-2">${book.summary}</p>
        <div class="flex flex-wrap gap-1.5 sm:gap-2 mb-3">
            ${book.keywords.split(',').slice(0, 3).map(kw => 
                `<span class="bg-gray-100 text-gray-700 px-2 py-1 rounded text-xs">${kw.trim()}</span>`
            ).join('')}
        </div>
        <div class="flex justify-between items-center gap-2">
            <span class="text-xs sm:text-sm ${book.available ? 'text-green-600' : 'text-red-600'}">
                <i class="fas fa-circle text-xs mr-1"></i>
                ${book.available ? 'Available' : 'Not Available'}
            </span>
            <button class="text-sm sm:text-base text-indigo-600 hover:text-indigo-800 font-semibold whitespace-nowrap">
                View Details <i class="fas fa-arrow-right ml-1"></i>
            </button>
        </div>
    `;
    
    card.addEventListener('click', () => showBookDetails(book));
    
    return card;
}

function showBookDetails(book) {
    const modal = document.getElementById('bookModal');
    const modalTitle = document.getElementById('modalTitle');
    const modalContent = document.getElementById('modalContent');
    
    modalTitle.textContent = book.title;
    
    modalContent.innerHTML = `
        <div class="space-y-3 sm:space-y-4">
            <div>
                <p class="text-xs sm:text-sm text-gray-600 mb-1">Author</p>
                <p class="text-base sm:text-lg font-semibold text-gray-800">${book.author}</p>
            </div>
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-3 sm:gap-4">
                <div>
                    <p class="text-xs sm:text-sm text-gray-600 mb-1">Category</p>
                    <span class="inline-block bg-indigo-100 text-indigo-800 px-2 sm:px-3 py-1 rounded-full text-xs sm:text-sm font-semibold">
                        ${book.category}
                    </span>
                </div>
                <div>
                    <p class="text-xs sm:text-sm text-gray-600 mb-1">Genre</p>
                    <span class="inline-block bg-purple-100 text-purple-800 px-2 sm:px-3 py-1 rounded-full text-xs sm:text-sm font-semibold">
                        ${book.genre}
                    </span>
                </div>
            </div>
            <div>
                <p class="text-xs sm:text-sm text-gray-600 mb-1">ISBN</p>
                <p class="text-sm sm:text-base text-gray-800 font-mono break-all">${book.isbn}</p>
            </div>
            <div>
                <p class="text-xs sm:text-sm text-gray-600 mb-2">Summary</p>
                <p class="text-sm sm:text-base text-gray-800 leading-relaxed">${book.summary}</p>
            </div>
            <div>
                <p class="text-xs sm:text-sm text-gray-600 mb-2">Keywords</p>
                <div class="flex flex-wrap gap-1.5 sm:gap-2">
                    ${book.keywords.split(',').map(kw => 
                        `<span class="bg-gray-100 text-gray-700 px-2 sm:px-3 py-1 rounded text-xs sm:text-sm">${kw.trim()}</span>`
                    ).join('')}
                </div>
            </div>
            <div class="pt-3 sm:pt-4 border-t">
                <p class="text-xs sm:text-sm text-gray-600 mb-2">Availability Status</p>
                <p class="text-base sm:text-lg font-semibold ${book.available ? 'text-green-600' : 'text-red-600'}">
                    <i class="fas fa-circle text-xs sm:text-sm mr-2"></i>
                    ${book.available ? 'Available for Borrowing' : 'Currently Not Available'}
                </p>
            </div>
            <div class="pt-3 sm:pt-4">
                <p class="text-xs sm:text-sm text-gray-600 mb-2">Rate this book</p>
                <div class="flex gap-1 sm:gap-2">
                    ${[1,2,3,4,5].map(rating => 
                        `<button onclick="rateBook(${book.id}, ${rating})" 
                                class="text-xl sm:text-2xl text-gray-300 hover:text-yellow-400 transition touch-manipulation">
                            <i class="fas fa-star"></i>
                        </button>`
                    ).join('')}
                </div>
            </div>
            <div class="pt-3 sm:pt-4">
                <button onclick="readBook(${book.id}, '${book.title.replace(/'/g, "\\'")}', '${book.author.replace(/'/g, "\\'")}')" 
                        class="w-full bg-green-600 hover:bg-green-700 text-white px-4 sm:px-6 py-3 rounded-lg font-semibold transition text-sm sm:text-base touch-manipulation">
                    <i class="fas fa-book-open mr-2"></i>Read This Book
                </button>
            </div>
        </div>
    `;
    
    modal.classList.remove('hidden');
}

function closeModal() {
    document.getElementById('bookModal').classList.add('hidden');
}

async function rateBook(bookId, rating) {
    try {
        await fetch(`${API_URL}/feedback`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ book_id: bookId, rating })
        });
        
        alert('Thank you for your feedback!');
        closeModal();
    } catch (error) {
        console.error('Error submitting feedback:', error);
        alert('Error submitting feedback');
    }
}

function showLoading(show) {
    const spinner = document.getElementById('loadingSpinner');
    const resultsSection = document.getElementById('resultsSection');
    
    if (show) {
        spinner.classList.remove('hidden');
        resultsSection.classList.add('hidden');
    } else {
        spinner.classList.add('hidden');
    }
}

async function readBook(bookId, title, author) {
    try {
        const response = await fetch(`${API_URL}/book/${bookId}/content`);
        const chapters = await response.json();
        
        if (!chapters || chapters.length === 0) {
            alert('This book content is not available for reading yet.');
            return;
        }
        
        currentBookData = { id: bookId, title, author };
        currentChapters = chapters;
        currentChapterIndex = 0;
        
        closeModal();
        openReader();
    } catch (error) {
        console.error('Error loading book content:', error);
        alert('Unable to load book content. Please try again.');
    }
}

function openReader() {
    const readerModal = document.getElementById('readerModal');
    document.getElementById('readerBookTitle').textContent = currentBookData.title;
    document.getElementById('readerBookAuthor').textContent = `by ${currentBookData.author}`;
    document.getElementById('totalChapters').textContent = currentChapters.length;
    
    displayChapter(0);
    readerModal.classList.remove('hidden');
}

function displayChapter(index) {
    if (index < 0 || index >= currentChapters.length) return;
    
    currentChapterIndex = index;
    const chapter = currentChapters[index];
    
    document.getElementById('readerChapterTitle').textContent = chapter.chapter_title;
    document.getElementById('readerContent').textContent = chapter.content;
    document.getElementById('currentChapter').textContent = index + 1;
    
    document.getElementById('prevChapter').disabled = index === 0;
    document.getElementById('nextChapter').disabled = index === currentChapters.length - 1;
}

function previousChapter() {
    if (currentChapterIndex > 0) {
        displayChapter(currentChapterIndex - 1);
    }
}

function nextChapter() {
    if (currentChapterIndex < currentChapters.length - 1) {
        displayChapter(currentChapterIndex + 1);
    }
}

function closeReader() {
    document.getElementById('readerModal').classList.add('hidden');
    currentBookData = null;
    currentChapters = [];
    currentChapterIndex = 0;
}

window.onclick = function(event) {
    const bookModal = document.getElementById('bookModal');
    const readerModal = document.getElementById('readerModal');
    
    if (event.target === bookModal) {
        closeModal();
    }
    if (event.target === readerModal) {
        closeReader();
    }
}

