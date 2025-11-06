import sqlite3
import os

class Database:
    def __init__(self, db_path='data/books.db'):
        self.db_path = db_path
        self.init_database()
    
    def get_connection(self):
        return sqlite3.connect(self.db_path)
    
    def init_database(self):
        os.makedirs('data', exist_ok=True)
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                category TEXT NOT NULL,
                genre TEXT,
                keywords TEXT,
                summary TEXT,
                isbn TEXT,
                available INTEGER DEFAULT 1
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS feedback (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                book_id INTEGER,
                rating INTEGER,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (book_id) REFERENCES books (id)
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS book_content (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                book_id INTEGER,
                chapter_number INTEGER,
                chapter_title TEXT,
                content TEXT,
                FOREIGN KEY (book_id) REFERENCES books (id)
            )
        ''')
        
        cursor.execute('SELECT COUNT(*) FROM books')
        if cursor.fetchone()[0] == 0:
            self.populate_sample_data(cursor)
            self.populate_sample_content(cursor)
        
        conn.commit()
        conn.close()
    
    def populate_sample_data(self, cursor):
        sample_books = [
            ('The Pragmatic Programmer', 'Andrew Hunt', 'Programming', 'Technology', 'software, development, best practices', 'A comprehensive guide to software development best practices and techniques.', '978-0135957059', 1),
            ('Clean Code', 'Robert C. Martin', 'Programming', 'Technology', 'code quality, refactoring, software', 'Learn how to write clean, maintainable, and efficient code.', '978-0132350884', 1),
            ('Introduction to Algorithms', 'Thomas H. Cormen', 'Computer Science', 'Technology', 'algorithms, data structures, complexity', 'Comprehensive coverage of algorithms and data structures.', '978-0262033848', 1),
            ('Artificial Intelligence: A Modern Approach', 'Stuart Russell', 'AI', 'Technology', 'machine learning, neural networks, AI', 'The most comprehensive, up-to-date introduction to AI.', '978-0134610993', 1),
            ('Deep Learning', 'Ian Goodfellow', 'Machine Learning', 'Technology', 'neural networks, deep learning, AI', 'An introduction to deep learning methods and applications.', '978-0262035613', 1),
            ('Python Crash Course', 'Eric Matthes', 'Programming', 'Technology', 'python, programming, beginner', 'A hands-on, project-based introduction to programming.', '978-1593279288', 1),
            ('The Art of Computer Programming', 'Donald Knuth', 'Computer Science', 'Technology', 'algorithms, programming, mathematics', 'Classic comprehensive monograph on computer programming.', '978-0201896831', 1),
            ('Design Patterns', 'Erich Gamma', 'Software Engineering', 'Technology', 'design patterns, object-oriented, architecture', 'Elements of reusable object-oriented software.', '978-0201633612', 1),
            ('Database System Concepts', 'Abraham Silberschatz', 'Database', 'Technology', 'database, SQL, DBMS', 'Comprehensive introduction to database systems.', '978-0078022159', 1),
            ('Computer Networks', 'Andrew Tanenbaum', 'Networks', 'Technology', 'networking, protocols, internet', 'Comprehensive guide to computer networking.', '978-0132126953', 1),
            ('Operating System Concepts', 'Abraham Silberschatz', 'Operating Systems', 'Technology', 'OS, processes, memory management', 'Fundamental concepts of operating systems.', '978-1118063330', 1),
            ('Thinking, Fast and Slow', 'Daniel Kahneman', 'Psychology', 'Science', 'cognitive psychology, decision making, behavior', 'Explores the two systems that drive the way we think.', '978-0374533557', 1),
            ('Sapiens', 'Yuval Noah Harari', 'History', 'Humanities', 'human history, evolution, civilization', 'A brief history of humankind from stone age to modern times.', '978-0062316097', 1),
            ('The Lean Startup', 'Eric Ries', 'Business', 'Management', 'entrepreneurship, innovation, startup', 'How constant innovation creates radically successful businesses.', '978-0307887894', 1),
            ('Atomic Habits', 'James Clear', 'Self Help', 'Personal Development', 'habits, productivity, improvement', 'An easy and proven way to build good habits and break bad ones.', '978-0735211292', 1),
            ('The Alchemist', 'Paulo Coelho', 'Fiction', 'Literature', 'adventure, philosophy, dreams', 'A magical tale about following your dreams.', '978-0062315007', 1),
            ('1984', 'George Orwell', 'Fiction', 'Literature', 'dystopia, surveillance, totalitarianism', 'A dystopian social science fiction novel.', '978-0451524935', 1),
            ('To Kill a Mockingbird', 'Harper Lee', 'Fiction', 'Literature', 'racism, justice, childhood', 'A classic of modern American literature.', '978-0061120084', 1),
            ('Brief History of Time', 'Stephen Hawking', 'Physics', 'Science', 'cosmology, universe, black holes', 'From the Big Bang to black holes.', '978-0553380163', 1),
            ('The Selfish Gene', 'Richard Dawkins', 'Biology', 'Science', 'evolution, genetics, biology', 'A gene-centered view of evolution.', '978-0198788607', 1),
            ('Data Science for Business', 'Foster Provost', 'Data Science', 'Technology', 'analytics, machine learning, business', 'What you need to know about data mining and data-analytic thinking.', '978-1449361327', 1),
            ('Web Development with Node and Express', 'Ethan Brown', 'Web Development', 'Technology', 'javascript, nodejs, backend', 'Leveraging the JavaScript stack for web development.', '978-1492053514', 1),
            ('React Up and Running', 'Stoyan Stefanov', 'Web Development', 'Technology', 'react, javascript, frontend', 'Building web applications with React.', '978-1492051459', 1),
            ('The Pragmatic Data Scientist', 'Stylianos Kampakis', 'Data Science', 'Technology', 'data analysis, statistics, ML', 'A practical guide to data science.', '978-1785887338', 1),
            ('Blockchain Basics', 'Daniel Drescher', 'Blockchain', 'Technology', 'cryptocurrency, distributed systems, blockchain', 'A non-technical introduction in 25 steps.', '978-1484226032', 1),
            ('Harry Potter and the Philosopher\'s Stone', 'J.K. Rowling', 'Fantasy', 'Fiction', 'magic, wizards, adventure, young adult', 'A young wizard discovers his magical heritage and begins his journey.', '978-0439708180', 1),
            ('The Lord of the Rings', 'J.R.R. Tolkien', 'Fantasy', 'Fiction', 'epic fantasy, adventure, middle earth', 'Epic tale of hobbits, elves, and the quest to destroy the One Ring.', '978-0544003415', 1),
            ('The Hobbit', 'J.R.R. Tolkien', 'Fantasy', 'Fiction', 'adventure, dragons, fantasy', 'Bilbo Baggins\' unexpected journey to reclaim treasure from a dragon.', '978-0547928227', 1),
            ('Dune', 'Frank Herbert', 'Science Fiction', 'Fiction', 'space, politics, desert planet', 'Epic science fiction saga about politics, religion, and ecology on a desert planet.', '978-0441172719', 1),
            ('Foundation', 'Isaac Asimov', 'Science Fiction', 'Fiction', 'space, empire, mathematics', 'Psychohistory predicts the fall of the Galactic Empire.', '978-0553293357', 1),
            ('The Martian', 'Andy Weir', 'Science Fiction', 'Fiction', 'space, survival, mars', 'An astronaut struggles to survive alone on Mars.', '978-0553418026', 1),
            ('Murder on the Orient Express', 'Agatha Christie', 'Mystery', 'Fiction', 'detective, murder, investigation', 'Hercule Poirot investigates a murder on a snowbound train.', '978-0062693662', 1),
            ('The Da Vinci Code', 'Dan Brown', 'Mystery', 'Fiction', 'thriller, conspiracy, history', 'A symbologist unravels a mystery involving secret societies.', '978-0307474278', 1),
            ('Gone Girl', 'Gillian Flynn', 'Thriller', 'Fiction', 'psychological, suspense, mystery', 'A woman disappears on her wedding anniversary.', '978-0307588371', 1),
            ('The Girl with the Dragon Tattoo', 'Stieg Larsson', 'Mystery', 'Fiction', 'crime, investigation, hacker', 'A journalist and hacker investigate a disappearance.', '978-0307949486', 1),
            ('Pride and Prejudice', 'Jane Austen', 'Romance', 'Fiction', 'classic, love, society', 'Classic tale of love and misunderstanding in Georgian England.', '978-0141439518', 1),
            ('The Notebook', 'Nicholas Sparks', 'Romance', 'Fiction', 'love, memory, relationships', 'A powerful story of enduring love.', '978-1455582877', 1),
            ('Dracula', 'Bram Stoker', 'Horror', 'Fiction', 'vampire, gothic, supernatural', 'Classic vampire novel featuring Count Dracula.', '978-0141439846', 1),
            ('The Shining', 'Stephen King', 'Horror', 'Fiction', 'supernatural, psychological, haunted', 'A family isolated in a haunted hotel during winter.', '978-0307743657', 1),
            ('It', 'Stephen King', 'Horror', 'Fiction', 'supernatural, fear, childhood', 'A group of kids face a shape-shifting evil entity.', '978-1501142970', 1),
            ('The Catcher in the Rye', 'J.D. Salinger', 'Literary Fiction', 'Fiction', 'coming of age, youth, alienation', 'A teenager\'s journey through alienation and identity crisis.', '978-0316769174', 1),
            ('Brave New World', 'Aldous Huxley', 'Dystopian', 'Fiction', 'future, society, control', 'A dystopian vision of a future society.', '978-0060850524', 1),
            ('The Handmaid\'s Tale', 'Margaret Atwood', 'Dystopian', 'Fiction', 'totalitarian, feminism, oppression', 'A woman\'s story in a totalitarian society.', '978-0385490818', 1),
            ('The Art of War', 'Sun Tzu', 'Philosophy', 'Military', 'strategy, tactics, warfare', 'Ancient Chinese military strategy and philosophy.', '978-1599869773', 1),
            ('Meditations', 'Marcus Aurelius', 'Philosophy', 'Classics', 'stoicism, wisdom, life', 'Personal writings of the Roman Emperor on Stoic philosophy.', '978-0812968255', 1),
            ('The Republic', 'Plato', 'Philosophy', 'Classics', 'justice, society, ethics', 'Socratic dialogue on justice and the ideal state.', '978-0872201361', 1),
            ('Thinking in Systems', 'Donella H. Meadows', 'Systems Theory', 'Science', 'complexity, systems, modeling', 'A primer on systems thinking and complex systems.', '978-1603580557', 1),
            ('The Elements of Statistical Learning', 'Trevor Hastie', 'Statistics', 'Technology', 'machine learning, statistics, data mining', 'Comprehensive resource on statistical learning methods.', '978-0387848570', 1),
            ('Gödel, Escher, Bach', 'Douglas Hofstadter', 'Computer Science', 'Science', 'consciousness, logic, mathematics', 'An exploration of consciousness through mathematics and art.', '978-0465026562', 1),
            ('The Code Book', 'Simon Singh', 'Cryptography', 'Technology', 'encryption, security, codes', 'The science of secrecy from ancient Egypt to quantum cryptography.', '978-0385495325', 1),
            ('Freakonomics', 'Steven Levitt', 'Economics', 'Business', 'economics, statistics, behavior', 'A rogue economist explores the hidden side of everything.', '978-0060731328', 1),
            ('Zero to One', 'Peter Thiel', 'Business', 'Entrepreneurship', 'startup, innovation, technology', 'Notes on startups and building the future.', '978-0804139298', 1),
            ('The Hard Thing About Hard Things', 'Ben Horowitz', 'Business', 'Management', 'leadership, startup, management', 'Building a business when there are no easy answers.', '978-0062273208', 1),
            ('Influence: The Psychology of Persuasion', 'Robert Cialdini', 'Psychology', 'Business', 'persuasion, influence, behavior', 'The psychology of why people say yes.', '978-0061241895', 1),
            ('Thinking in Bets', 'Annie Duke', 'Decision Making', 'Self Help', 'decision making, probability, thinking', 'Making smarter decisions when you don\'t have all the facts.', '978-0735216358', 1),
            ('The Black Swan', 'Nassim Nicholas Taleb', 'Philosophy', 'Business', 'risk, probability, randomness', 'The impact of highly improbable events.', '978-0812973815', 1),
            ('Educated', 'Tara Westover', 'Biography', 'Memoir', 'education, family, transformation', 'A memoir about a young woman who leaves her survivalist family.', '978-0399590504', 1),
            ('Steve Jobs', 'Walter Isaacson', 'Biography', 'Technology', 'apple, innovation, leadership', 'The exclusive biography of Steve Jobs.', '978-1451648539', 1),
            ('The Immortal Life of Henrietta Lacks', 'Rebecca Skloot', 'Biography', 'Science', 'medical ethics, cells, research', 'The story behind the immortal HeLa cell line.', '978-1400052189', 1),
            ('Cosmos', 'Carl Sagan', 'Astronomy', 'Science', 'space, universe, science', 'A journey through space and time exploring the cosmos.', '978-0345539434', 1),
            ('A Short History of Nearly Everything', 'Bill Bryson', 'Science', 'Popular Science', 'science, history, universe', 'Understanding the universe and our place in it.', '978-0767908184', 1),
            ('The Gene', 'Siddhartha Mukherjee', 'Biology', 'Science', 'genetics, DNA, heredity', 'An intimate history of genetics and the future of medicine.', '978-1476733524', 1),
            ('The Origin of Species', 'Charles Darwin', 'Biology', 'Science', 'evolution, natural selection, biology', 'Darwin\'s groundbreaking work on evolution.', '978-0451529060', 1),
            ('Guns, Germs, and Steel', 'Jared Diamond', 'History', 'Anthropology', 'civilization, geography, history', 'The fates of human societies and why some prospered.', '978-0393317558', 1),
            ('The Power of Now', 'Eckhart Tolle', 'Spirituality', 'Self Help', 'mindfulness, presence, consciousness', 'A guide to spiritual enlightenment and living in the present.', '978-1577314806', 1),
            ('Man\'s Search for Meaning', 'Viktor Frankl', 'Psychology', 'Philosophy', 'existentialism, meaning, suffering', 'A psychiatrist\'s account of life in Nazi death camps.', '978-0807014295', 1),
            ('The 7 Habits of Highly Effective People', 'Stephen Covey', 'Self Help', 'Business', 'productivity, habits, success', 'Powerful lessons in personal change and effectiveness.', '978-1982137274', 1),
            ('Good to Great', 'Jim Collins', 'Business', 'Management', 'leadership, business strategy, success', 'Why some companies make the leap and others don\'t.', '978-0066620992', 1),
            ('Shoe Dog', 'Phil Knight', 'Biography', 'Business', 'entrepreneurship, nike, memoir', 'The memoir of Nike\'s founder Phil Knight.', '978-1501135927', 1),
            ('The Everything Store', 'Brad Stone', 'Biography', 'Business', 'amazon, ecommerce, technology', 'Jeff Bezos and the age of Amazon.', '978-0316219266', 1),
            ('Outliers', 'Malcolm Gladwell', 'Psychology', 'Sociology', 'success, achievement, culture', 'The story of success and what makes high-achievers different.', '978-0316017930', 1),
            ('Thinking, Fast and Slow', 'Daniel Kahneman', 'Psychology', 'Science', 'cognitive science, decision making, behavior', 'The two systems that drive the way we think.', '978-0374533557', 1)
        ]
        
        cursor.executemany('''
            INSERT INTO books (title, author, category, genre, keywords, summary, isbn, available)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', sample_books)
    
    def get_all_books(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM books')
        books = [dict(zip([col[0] for col in cursor.description], row)) for row in cursor.fetchall()]
        conn.close()
        return books
    
    def get_categories(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT DISTINCT category FROM books ORDER BY category')
        categories = [row[0] for row in cursor.fetchall()]
        conn.close()
        return categories
    
    def search_books(self, query, category=''):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        if category:
            cursor.execute('''
                SELECT * FROM books 
                WHERE category = ? AND (title LIKE ? OR author LIKE ? OR keywords LIKE ?)
            ''', (category, f'%{query}%', f'%{query}%', f'%{query}%'))
        else:
            cursor.execute('''
                SELECT * FROM books 
                WHERE title LIKE ? OR author LIKE ? OR keywords LIKE ? OR summary LIKE ?
            ''', (f'%{query}%', f'%{query}%', f'%{query}%', f'%{query}%'))
        
        books = [dict(zip([col[0] for col in cursor.description], row)) for row in cursor.fetchall()]
        conn.close()
        return books
    
    def get_book_by_id(self, book_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM books WHERE id = ?', (book_id,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return dict(zip([col[0] for col in cursor.description], row))
        return None
    
    def add_feedback(self, book_id, rating):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO feedback (book_id, rating) VALUES (?, ?)', (book_id, rating))
        conn.commit()
        conn.close()
    
    def get_book_content(self, book_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT chapter_number, chapter_title, content 
            FROM book_content 
            WHERE book_id = ? 
            ORDER BY chapter_number
        ''', (book_id,))
        chapters = [dict(zip([col[0] for col in cursor.description], row)) for row in cursor.fetchall()]
        conn.close()
        return chapters
    
    def populate_sample_content(self, cursor):
        sample_content = []
        
        # Generate content for all 73 books
        content_data = [
            (1, 'Introduction', 'Welcome to "The Pragmatic Programmer"! This book is about the essence of good programming - the pragmatic approach to software development. Throughout this journey, we\'ll explore fundamental principles that separate exceptional programmers from average ones.\n\nProgramming is a craft. At its simplest, it is about getting a computer to do what you want it to do. As a programmer, you\'re part listener, part advisor, part interpreter, and part dictator.\n\nKey topics we\'ll cover:\n- The importance of taking responsibility\n- Software entropy and how to combat it\n- The DRY principle\n- Orthogonality in system design\n- Reversibility and flexibility'),
            
            (2, 'Introduction to Clean Code', 'You are reading this book for two reasons. First, you are a programmer. Second, you want to be a better programmer. Good. We need better programmers.\n\nThis is a book about good programming. It is filled with code. We\'re going to look at code from every angle.\n\nThe code quality is important because:\n1. Bad code can bring a company down\n2. We\'ve all been slowed down by messy code\n3. We\'ve all felt the relief of working in clean code\n\nClean code always looks like it was written by someone who cares.'),
            
            (3, 'The Role of Algorithms in Computing', 'Algorithms are at the heart of every nontrivial computer application. This book provides a comprehensive introduction to the modern study of computer algorithms.\n\nWhat are algorithms? Informally, an algorithm is any well-defined computational procedure that takes some value, or set of values, as input and produces some value, or set of values, as output.\n\nFor example, suppose we need to sort a sequence of numbers into nondecreasing order. This problem arises frequently in practice and provides fertile ground for introducing many standard design techniques and analysis tools.'),
            
            (4, 'Chapter 1: Intelligent Systems', 'Artificial Intelligence: A Modern Approach is the leading textbook in Artificial Intelligence. This chapter introduces the foundations of AI and the concept of intelligent agents.\n\nWhat is AI? Different people approach AI with different goals in mind. We need to consider four possible approaches: thinking humanly, thinking rationally, acting humanly, and acting rationally.\n\nAn agent is anything that can be viewed as perceiving its environment through sensors and acting upon that environment through actuators. The notion of an agent is meant to be a tool for analyzing systems, not an absolute characterization that divides the world into agents and non-agents.'),
            
            (5, 'Introduction to Deep Learning', 'Deep learning is a form of machine learning that enables computers to learn from experience and understand the world in terms of a hierarchy of concepts. Because the computer gathers knowledge from experience, there is no need for a human computer operator to formally specify all the knowledge that the computer needs.\n\nThe hierarchy of concepts allows the computer to learn complicated concepts by building them out of simpler ones. If we draw a graph showing how these concepts are built on top of each other, the graph is deep, with many layers. For this reason, we call this approach to AI deep learning.'),
            
            (6, 'Getting Started with Python', 'Python Crash Course is a fast-paced, thorough introduction to programming with Python that will have you writing programs, solving problems, and making things that work in no time.\n\nIn the first half of the book, you\'ll learn basic programming concepts such as variables, lists, classes, and loops, and practice writing clean code with exercises for each topic. You\'ll also learn to make your programs interactive and test your code safely before adding it to a project.\n\nIn the second half, you\'ll put your new knowledge into practice with three substantial projects: a Space Invaders-inspired arcade game, a set of data visualizations with Python\'s handy libraries, and a simple web app you can deploy online.'),
            
            (7, 'Fundamental Algorithms', 'The Art of Computer Programming is a comprehensive monograph written by computer scientist Donald Knuth that covers many kinds of programming algorithms and their analysis.\n\nKnuth began the project, originally conceived as a single book with twelve chapters, in 1962. The first three volumes of what was then expected to be a seven-volume set were published in 1968, 1969, and 1973.\n\nThe book has influenced many areas of computer science, including:\n- Algorithm design and analysis\n- Data structures\n- Complexity theory\n- Compilation techniques'),
            
            (8, 'Introduction to Design Patterns', 'Design patterns are solutions to commonly occurring problems in software design. This book introduces 23 classic software design patterns.\n\nPatterns are discovered, not invented. The patterns in this book are solutions that have evolved over time. They emerged from the real-world experiences of skilled software designers.\n\nThe pattern catalog includes:\n- Creational patterns: Abstract Factory, Builder, Factory Method, Prototype, Singleton\n- Structural patterns: Adapter, Bridge, Composite, Decorator, Facade, Flyweight, Proxy\n- Behavioral patterns: Chain of Responsibility, Command, Interpreter, Iterator, Mediator, Memento, Observer, State, Strategy, Template Method, Visitor'),
            
            (9, 'Database Fundamentals', 'Database System Concepts presents the fundamental concepts of database management. This comprehensive book covers both traditional and emerging database topics.\n\nA database-management system (DBMS) is a collection of interrelated data and a set of programs to access those data. The collection of data is usually referred to as the database, and it contains information relevant to an enterprise.\n\nThe primary goal of a DBMS is to provide a way to store and retrieve database information that is both convenient and efficient.'),
            
            (10, 'Networking Fundamentals', 'Computer Networks provides a comprehensive introduction to the modern computer networking field. This book uses the Internet as the primary example of computer networks.\n\nThe material is organized according to the five-layer Internet protocol stack:\n- Application layer\n- Transport layer\n- Network layer\n- Link layer\n- Physical layer\n\nEach layer is examined in detail, exploring its functionality, protocols, and implementation.'),
            
            (11, 'Operating System Concepts', 'Operating System Concepts provides a solid theoretical foundation for understanding operating systems. The book presents core concepts and algorithms in detail, covering process management, memory management, storage management, protection, and security.\n\nAn operating system acts as an intermediary between the user of a computer and the computer hardware. The purpose of an operating system is to provide an environment in which a user can execute programs in a convenient and efficient manner.'),
            
            (12, 'Understanding Human Thought', 'In Thinking, Fast and Slow, Daniel Kahneman takes us on a groundbreaking tour of the mind and explains the two systems that drive the way we think.\n\nSystem 1 is fast, intuitive, and emotional. System 2 is slower, more deliberative, and more logical. The book examines how these two systems shape our judgments and decisions, revealing where we can and cannot trust our intuitions.\n\nKey concepts include cognitive biases, prospect theory, and the concept of "what you see is all there is" (WYSIATI).'),
            
            (13, 'A Brief History of Humankind', 'Sapiens explores how Homo sapiens came to dominate the world. The book examines our species from the emergence of Homo sapiens in Africa up to the present.\n\nHarari describes three major revolutions in human history:\n- The Cognitive Revolution (70,000 years ago)\n- The Agricultural Revolution (12,000 years ago)\n- The Scientific Revolution (500 years ago)\n\nThese revolutions have empowered humans to do something no other form of life has done: create and connect around ideas that do not physically exist.'),
            
            (14, 'Innovation and Entrepreneurship', 'The Lean Startup methodology reconceives a company\'s efforts to spend less money and time developing new products or services. The methodology aims to eliminate wasteful practices and increase value-producing practices during the product development phase.\n\nThe key principles include:\n- Build-Measure-Learn feedback loop\n- Validated learning\n- Minimum Viable Product (MVP)\n- Innovation accounting\n- Pivot or persevere decisions'),
            
            (15, 'Building Better Habits', 'Atomic Habits reveals practical strategies that will teach you exactly how to form good habits, break bad ones, and master the tiny behaviors that lead to remarkable results.\n\nThe book is based on four laws:\n1. Make it obvious\n2. Make it attractive\n3. Make it easy\n4. Make it satisfying\n\nIf you\'re having trouble changing your habits, the problem isn\'t you. The problem is your system. Bad habits repeat themselves not because you don\'t want to change, but because you have the wrong system for change.'),
            
            (16, 'The Journey to Your Personal Legend', 'The Alchemist tells the story of Santiago, an Andalusian shepherd boy who dreams of finding treasure. His quest will lead him to riches far different—and far more satisfying—than he ever imagined.\n\nThe book explores themes of following your dreams, recognizing opportunity, learning to read omens, and listening to your heart. The central message is about the importance of pursuing your Personal Legend and listening to your heart.'),
            
            (17, 'A Dystopian Masterpiece', 'George Orwell\'s 1984 is a dystopian novel published in 1949. The story takes place in an imagined future, the year 1984, when much of the world has fallen victim to perpetual war, omnipresent government surveillance, historical negationism, and propaganda.\n\nKey concepts include:\n- Big Brother and totalitarian surveillance\n- Thoughtcrime and the Thought Police\n- Doublethink and Newspeak\n- The mutability of history\n\nThe novel explores themes of truth, freedom, and individuality in a totalitarian state.'),
            
            (18, 'Justice and Moral Growth', 'To Kill a Mockingbird is set in the fictional town of Maycomb, Alabama, during the Great Depression. The story explores human behavior and the collective conscience of the American South.\n\nThrough the eyes of Scout Finch, we witness her father Atticus defend a Black man falsely accused of a crime. The novel explores themes of racial injustice, moral growth, and the coexistence of good and evil.\n\nIt remains one of the most important works of American literature, teaching compassion, empathy, and the importance of moral courage.'),
            
            (19, 'From the Big Bang to Black Holes', 'A Brief History of Time explores the nature of space and time, the role of God in creation, the history and future of the universe.\n\nStephen Hawking addresses questions such as:\n- Was there a beginning of time?\n- Will there be an end?\n- Is the universe infinite?\n- Where did it come from?\n\nThe book covers topics including black holes, the origin and fate of the universe, quantum mechanics, and the search for a unified theory of physics.'),
            
            (20, 'The Gene-Centered View of Evolution', 'The Selfish Gene revolutionized our understanding of evolution. Richard Dawkins argues that natural selection operates at the level of genes, not individuals or groups.\n\nKey concepts include:\n- Genes as the unit of selection\n- The concept of memes\n- Evolutionary stable strategies\n- The extended phenotype\n\nThe book explains how genes use bodies as "survival machines" to ensure their own propagation.'),
            
            (21, 'Data Science in Practice', 'Data Science for Business provides a comprehensive introduction to the fundamental principles of data science. It helps readers understand data-analytic thinking and how it can add value to their organizations.\n\nKey topics include:\n- Data mining and predictive modeling\n- Classification and regression\n- Clustering and similarity matching\n- Co-occurrence grouping\n- Profiling and behavior prediction\n\nThe book emphasizes understanding the fundamental concepts behind data science rather than specific tools.'),
            
            (22, 'Building Web Applications with Node.js', 'Web Development with Node and Express teaches you how to build dynamic web applications using Node.js and the Express framework.\n\nExpress is a minimal and flexible Node.js web application framework that provides a robust set of features for web and mobile applications.\n\nYou\'ll learn to:\n- Set up a Node.js development environment\n- Create and configure Express applications\n- Handle routing and middleware\n- Work with templates and views\n- Implement authentication and security'),
            
            (23, 'Modern JavaScript Development', 'React Up and Running teaches you how to build dynamic web applications with React, the popular JavaScript library maintained by Facebook.\n\nReact allows developers to create large web applications that can update and render efficiently in response to data changes. The key feature is the ability to build components that manage their own state.\n\nYou\'ll learn:\n- JSX syntax\n- Component lifecycle\n- State and props\n- Event handling\n- Working with forms'),
            
            (24, 'Practical Data Science', 'The Pragmatic Data Scientist provides a practical guide to data science. It covers the entire data science workflow from problem formulation to model deployment.\n\nThe book emphasizes:\n- Understanding business problems\n- Data collection and cleaning\n- Exploratory data analysis\n- Model building and validation\n- Communicating results effectively\n\nSuccess in data science requires both technical skills and business acumen.'),
            
            (25, 'Understanding Blockchain Technology', 'Blockchain Basics explains blockchain technology in 25 concise steps. This non-technical introduction helps readers understand the fundamental concepts behind blockchain and cryptocurrencies.\n\nKey topics include:\n- Distributed ledgers\n- Cryptographic hashing\n- Consensus mechanisms\n- Smart contracts\n- Use cases beyond cryptocurrency\n\nThe book demystifies blockchain technology and explains its potential applications across various industries.'),
            
            (26, 'The Wizarding World Begins', 'Harry Potter and the Philosopher\'s Stone introduces us to the magical world of wizards and witches. Young Harry Potter discovers he is a wizard on his eleventh birthday and begins his education at Hogwarts School of Witchcraft and Wizardry.\n\nIn his first year, Harry makes new friends, learns magic, plays Quidditch, and discovers the truth about his past. He also faces the dark wizard who killed his parents and left him with a lightning-bolt scar.\n\nThe story explores themes of friendship, bravery, and the battle between good and evil.'),
            
            (27, 'The Fellowship of the Ring', 'The Lord of the Rings tells the epic tale of the One Ring and the quest to destroy it in the fires of Mount Doom. When the hobbit Frodo Baggins inherits a mysterious ring from his uncle Bilbo, he learns it is the One Ring, forged by the Dark Lord Sauron to control all other rings of power.\n\nFrodo must leave the Shire and embark on a perilous journey to Rivendell, where the Council of Elrond decides the Ring must be destroyed. A fellowship is formed to help Frodo on his quest, consisting of hobbits, elves, dwarves, and men.'),
            
            (28, 'There and Back Again', 'The Hobbit follows Bilbo Baggins, a comfort-loving hobbit, on an unexpected adventure with a company of dwarves led by Thorin Oakenshield.\n\nTheir quest: to reclaim the Lonely Mountain and its treasure from the dragon Smaug. Along the way, Bilbo discovers courage he never knew he had and finds a mysterious ring that will change the course of Middle-earth.\n\nThe journey transforms Bilbo from a provincial hobbit into a hero, teaching him about bravery, friendship, and the wider world beyond the Shire.'),
            
            (29, 'Politics and Power on Arrakis', 'Dune is set in the distant future amidst a sprawling feudal interstellar empire. The story follows young Paul Atreides, whose family accepts stewardship of the desert planet Arrakis, the only source of the "spice" melange, the most valuable substance in the universe.\n\nThe novel explores themes of politics, religion, ecology, and human evolution. It presents a complex universe with intricate systems of government, economics, and belief.\n\nPaul must navigate betrayal, face his destiny, and embrace his role in a centuries-old prophecy.'),
            
            (30, 'Psychohistory and the Fall of Empire', 'Foundation tells the story of mathematician Hari Seldon, who develops psychohistory—a mathematical sociology that can predict the future of large populations.\n\nSeldon foresees the fall of the Galactic Empire and thirty thousand years of barbarism. To preserve knowledge and shorten this dark age, he establishes two Foundations at opposite ends of the galaxy.\n\nThe novel follows the first Foundation through several crises as it grows from a small community of scientists into a major power in the galaxy.'),
            
            (31, 'Survival on Mars', 'The Martian tells the story of astronaut Mark Watney, who is presumed dead and left behind on Mars after a dust storm forces his crew to evacuate.\n\nWith only limited supplies and his ingenuity, Watney must find a way to survive on the hostile planet while signaling to Earth that he\'s alive. He must solve impossible problems, one by one, to have any hope of rescue.\n\nThe novel celebrates human ingenuity, the scientific method, and the indomitable human spirit in the face of overwhelming odds.'),
            
            (32, 'Murder on a Train', 'Murder on the Orient Express features Belgian detective Hercule Poirot, who finds himself investigating a murder aboard the luxurious Orient Express.\n\nWhen a wealthy passenger is found stabbed to death in his locked compartment, Poirot must solve the case before the train reaches its destination. Every passenger becomes a suspect, and Poirot discovers that almost everyone has a connection to the victim.\n\nThe solution to this mystery is one of Christie\'s most brilliant and surprising.'),
            
            (33, 'Symbols and Secrets', 'The Da Vinci Code follows symbologist Robert Langdon as he investigates a murder in the Louvre Museum. The investigation leads him to discover clues hidden in the works of Leonardo da Vinci.\n\nLangdon teams up with cryptologist Sophie Neveu to solve a series of puzzles. Their quest unveils a conspiracy involving the Priory of Sion and the Knights Templar, centered around a secret that could shake the foundations of Christianity.\n\nThe novel combines art history, codes, and conspiracy theories into a thrilling narrative.'),
            
            (34, 'The Perfect Marriage?', 'Gone Girl tells the story of Nick and Amy Dunne\'s troubled marriage. On their fifth wedding anniversary, Amy disappears, and Nick becomes the prime suspect.\n\nThe novel alternates between Nick\'s present-day narrative and Amy\'s diary entries, gradually revealing the dark truths beneath their seemingly perfect relationship.\n\nThis psychological thriller explores themes of marriage, identity, and the public persona versus private reality. The twists and turns keep readers questioning everything they think they know.'),
            
            (35, 'Digital Vengeance', 'The Girl with the Dragon Tattoo introduces Lisbeth Salander, a brilliant but troubled hacker, and Mikael Blomkvist, an investigative journalist.\n\nBlomkvist is hired to solve a forty-year-old mystery: the disappearance of Harriet Vanger. As he digs deeper, he uncovers a dark history of violence and abuse. With Salander\'s help, he pieces together a story more disturbing than he imagined.\n\nThe novel combines mystery, family saga, and social commentary on violence against women.'),
            
            (36, 'First Impressions', 'Pride and Prejudice follows Elizabeth Bennet as she deals with issues of manners, upbringing, morality, education, and marriage in the landed gentry of early 19th-century England.\n\nElizabeth initially dislikes the proud Mr. Darcy, but as she learns more about him, her feelings begin to change. The novel explores how first impressions can be deceiving and how pride and prejudice can cloud judgment.\n\nAusten\'s wit and social commentary make this a timeless examination of class, marriage, and society.'),
            
            (37, 'Enduring Love', 'The Notebook tells the story of Noah and Allie, whose love story spans decades. Noah is a country boy who falls in love with Allie, a wealthy girl spending the summer in his town.\n\nDespite their different backgrounds, they fall deeply in love. When they\'re separated, Noah writes Allie 365 letters over a year. Years later, they meet again, and their love is rekindled.\n\nThe novel explores themes of true love, memory, and the power of devotion that transcends time.'),
            
            (38, 'The Undead Legend', 'Dracula is the classic vampire novel told through letters, diary entries, and newspaper articles. Jonathan Harker travels to Transylvania to help Count Dracula with a real estate transaction.\n\nHarker soon realizes he is a prisoner and that Dracula is a vampire planning to move to England. When Dracula arrives in England, a group led by Professor Van Helsing must track and destroy him.\n\nThe novel established many conventions of vampire literature and explores themes of sexuality, immigration, and the conflict between traditional and modern beliefs.'),
            
            (39, 'Winter at the Overlook', 'The Shining tells the story of Jack Torrance, who becomes winter caretaker of the isolated Overlook Hotel in Colorado with his wife Wendy and son Danny.\n\nDanny has psychic abilities called "the shining" that allow him to see the hotel\'s horrific past. As winter progresses, the hotel\'s evil influences drive Jack toward madness and violence.\n\nThe novel explores themes of addiction, domestic violence, and the supernatural, creating one of the most terrifying stories in horror literature.'),
            
            (40, 'We All Float', 'It tells the story of seven children in Derry, Maine, who are terrorized by a shape-shifting evil entity that exploits the fears of its victims.\n\nThe entity, which usually appears as Pennywise the Dancing Clown, awakens every 27 years to feed. The children, who call themselves the Losers Club, must confront their fears to defeat It.\n\nThe novel alternates between their childhood in 1958 and their reunion as adults in 1985 when It returns. It explores themes of childhood trauma, friendship, and the power of memory.'),
            
            (41, 'Adolescent Alienation', 'The Catcher in the Rye follows Holden Caulfield, a teenager expelled from prep school, during three days in New York City.\n\nHolden struggles with growing up and fitting into adult society. He sees the adult world as full of "phonies" and hypocrisy. His narrative reveals his conflicted feelings about childhood, sexuality, and identity.\n\nThe novel explores themes of alienation, innocence, and the painful transition from childhood to adulthood. Holden\'s voice has resonated with generations of readers.'),
            
            (42, 'A Perfectly Ordered World', 'Brave New World presents a futuristic World State where citizens are engineered through artificial wombs and childhood conditioning into predetermined classes.\n\nSociety is designed for stability and happiness, achieved through genetic engineering, infant conditioning, and a pleasure drug called soma. Bernard Marx, an Alpha-Plus psychologist, begins to question this seemingly perfect society.\n\nThe novel explores themes of technology, freedom, individuality, and the price of happiness and stability.'),
            
            (43, 'Life in Gilead', 'The Handmaid\'s Tale is set in the Republic of Gilead, a totalitarian theocracy that has overthrown the United States government.\n\nThe story follows Offred, a Handmaid whose sole function is to breed for the ruling class. Through her eyes, we see the systematic oppression of women and the erasure of individual identity.\n\nThe novel explores themes of power, gender, religion, and resistance. It remains a powerful warning about fundamentalism and the fragility of freedom.'),
            
            (44, 'Ancient Military Strategy', 'The Art of War is an ancient Chinese military treatise dating from the 5th century BC. Attributed to Sun Tzu, a military strategist and general, it addresses strategy, tactics, and leadership.\n\nKey principles include:\n- Know your enemy and know yourself\n- All warfare is based on deception\n- Supreme excellence consists of breaking the enemy\'s resistance without fighting\n- Appear weak when you are strong\n\nWhile written for military conflicts, its principles have been applied to business, sports, and life strategy.'),
            
            (45, 'Stoic Wisdom', 'Meditations is a series of personal writings by Marcus Aurelius, Roman Emperor from 161 to 180 AD. The work comprises his private notes to himself and ideas on Stoic philosophy.\n\nKey Stoic principles include:\n- Focus on what you can control\n- Accept what you cannot change\n- Live in accordance with nature\n- Practice virtue and wisdom\n\nThese reflections provide timeless insights on how to live a good and meaningful life.'),
            
            (46, 'Justice and the Ideal State', 'The Republic is Plato\'s most famous work, a Socratic dialogue concerning justice and the ideal state. Socrates and others discuss the meaning of justice and whether the just man is happier than the unjust man.\n\nThe work includes Plato\'s Allegory of the Cave, a meditation on knowledge and reality. It also presents the concept of philosopher-kings who should rule the ideal state.\n\nThe Republic explores ethics, politics, epistemology, and metaphysics, establishing foundations for Western philosophy.'),
            
            (47, 'Understanding Complex Systems', 'Thinking in Systems introduces the essential systems thinking skills. A system is a set of things—people, cells, molecules—interconnected in such a way that they produce their own pattern of behavior over time.\n\nKey concepts include:\n- Stocks and flows\n- Feedback loops\n- Leverage points\n- System archetypes\n\nSystems thinking helps us understand how to intervene effectively in complex systems and avoid unintended consequences.'),
            
            (48, 'Statistical Learning Methods', 'The Elements of Statistical Learning describes important concepts in modern statistics and machine learning. It covers supervised learning, unsupervised learning, and statistical inference.\n\nTopics include:\n- Linear methods for regression and classification\n- Basis expansions and regularization\n- Kernel methods\n- Model assessment and selection\n- Ensemble methods\n\nThis comprehensive reference has become essential for researchers and practitioners in machine learning.'),
            
            (49, 'An Eternal Golden Braid', 'Gödel, Escher, Bach explores how cognition emerges from hidden neurological mechanisms. The book draws connections between the music of Bach, the artwork of Escher, and Gödel\'s Incompleteness Theorems.\n\nIt introduces concepts like:\n- Strange loops\n- Self-reference\n- Formal systems\n- Consciousness and AI\n\nThe book argues that consciousness arises from self-referential patterns in the brain.'),
            
            (50, 'The Science of Secrecy', 'The Code Book chronicles the evolution of cryptography from ancient Egypt to quantum cryptography. It tells the story of codes and codebreaking throughout history.\n\nKey topics include:\n- Caesar cipher and substitution ciphers\n- The Enigma machine\n- Public key cryptography\n- Quantum cryptography\n\nThe book shows how cryptography has influenced military battles, political intrigue, and now protects our digital lives.'),
            
            (51, 'Hidden Economics', 'Freakonomics explores the hidden side of everything using economic thinking and data analysis. It shows how incentives shape human behavior in surprising ways.\n\nKey questions examined:\n- What do schoolteachers and sumo wrestlers have in common?\n- Why do drug dealers still live with their moms?\n- How much do parents really matter?\n\nThe book demonstrates how economic analysis can reveal unexpected truths about human behavior.'),
            
            (52, 'Building the Future', 'Zero to One presents Peter Thiel\'s philosophy on startups and innovation. The key insight: copying what works takes the world from 1 to n, but creating something new takes the world from 0 to 1.\n\nKey principles:\n- Competition is for losers\n- Create monopolies through innovation\n- Technology and globalization are different\n- Last mover advantage\n\nThe book challenges conventional wisdom about business and entrepreneurship.'),
            
            (53, 'Navigating Difficult Decisions', 'The Hard Thing About Hard Things offers practical wisdom for running a startup or business. Ben Horowitz shares his experiences building and selling companies.\n\nKey insights:\n- Managing in peacetime vs wartime\n- Making layoffs\n- Demoting loyal friends\n- Dealing with crisis\n\nThe book provides honest advice on the hardest problems CEOs face, for which there are no formulaic solutions.'),
            
            (54, 'The Psychology of Persuasion', 'Influence explains the psychology of why people say yes and how to apply these principles ethically. Robert Cialdini identifies six principles of persuasion.\n\nThe six principles:\n1. Reciprocity\n2. Commitment and Consistency\n3. Social Proof\n4. Authority\n5. Liking\n6. Scarcity\n\nUnderstanding these principles helps us recognize when we\'re being influenced and how to influence others responsibly.'),
            
            (55, 'Making Smarter Decisions', 'Thinking in Bets applies poker thinking to decision-making. Annie Duke, a professional poker player, shows how to make better decisions under uncertainty.\n\nKey concepts:\n- Resulting: judging decisions by outcomes\n- Probabilistic thinking\n- Updating beliefs\n- Mental time travel\n\nThe book teaches us to think in terms of probabilities and to separate decision quality from outcome quality.'),
            
            (56, 'The Impact of the Improbable', 'The Black Swan explores the extreme impact of rare and unpredictable events. Nassim Taleb argues that much of what happens in the world is due to Black Swan events.\n\nKey concepts:\n- Black Swans: rare, high-impact events\n- Narrative fallacy\n- Confirmation bias\n- Antifragility\n\nThe book challenges our assumptions about predictability and shows how we underestimate randomness and overestimate our knowledge.'),
            
            (57, 'A Memoir of Transformation', 'Educated is Tara Westover\'s memoir of growing up in a survivalist family in rural Idaho and her journey to education. Despite not attending school, she taught herself enough to gain admission to Brigham Young University.\n\nHer story explores:\n- The power of education\n- Family loyalty vs personal growth\n- Overcoming the past\n- Self-invention\n\nThe memoir is a testament to the transformative power of learning and the difficulty of breaking from one\'s past.'),
            
            (58, 'Innovation and Leadership', 'Steve Jobs is the authorized biography based on interviews with Jobs, his family, colleagues, and competitors. It provides an intimate look at the man who co-founded Apple and revolutionized multiple industries.\n\nThe biography covers:\n- Jobs\' early life and founding of Apple\n- His ousting and return to Apple\n- Creation of revolutionary products\n- His management style and vision\n\nIt reveals both his genius and his complex, often difficult personality.'),
            
            (59, 'Science and Medical Ethics', 'The Immortal Life of Henrietta Lacks tells the story of an African American woman whose cancer cells were taken without her knowledge in 1951.\n\nThese HeLa cells became one of the most important tools in medicine, leading to breakthroughs in vaccines, cloning, gene mapping, and more. Yet Henrietta\'s family knew nothing about this for decades.\n\nThe book explores medical ethics, racism, informed consent, and the human story behind scientific advancement.'),
            
            (60, 'The Universe Explored', 'Cosmos accompanies Carl Sagan\'s acclaimed television series. It explores fifteen billion years of cosmic evolution and the development of science and civilization.\n\nTopics include:\n- The origin of life\n- The cosmos and our place in it\n- The search for extraterrestrial life\n- The future of humanity\n\nSagan\'s passionate and poetic writing makes complex scientific concepts accessible and inspiring.'),
            
            (61, 'Understanding Our World', 'A Short History of Nearly Everything attempts to explain complex scientific concepts in layman\'s terms. Bill Bryson explores how we came to know what we know about the world.\n\nTopics covered:\n- The Big Bang\n- The formation of Earth\n- The development of life\n- Human evolution\n\nBryson makes science engaging through storytelling and humor, while maintaining scientific accuracy.'),
            
            (62, 'An Intimate History', 'The Gene is the story of one of the most powerful and dangerous ideas in human history. Siddhartha Mukherjee traces the history of genetics from Mendel\'s peas to modern gene editing.\n\nThe book explores:\n- The discovery of genes\n- Nature vs nurture\n- Genetic diseases\n- The future of genetic engineering\n\nIt weaves together science, history, and personal narrative to illuminate the profound implications of genetic knowledge.'),
            
            (63, 'Natural Selection', 'The Origin of Species introduced the scientific theory that populations evolve through natural selection. Darwin\'s revolutionary work fundamentally changed our understanding of life on Earth.\n\nKey concepts:\n- Natural selection\n- Descent with modification\n- Survival of the fittest\n- Common ancestry\n\nThe book provided overwhelming evidence for evolution and established it as the organizing principle of biology.'),
            
            (64, 'The Fates of Human Societies', 'Guns, Germs, and Steel asks why Eurasia and North Africa dominated the world rather than other continents. Jared Diamond argues that environmental and geographical factors shaped the modern world.\n\nKey factors:\n- Domesticable plants and animals\n- Geographic orientation\n- Disease immunity\n- Technology diffusion\n\nThe book challenges racist explanations of history by showing how environmental factors drove human development.'),
            
            (65, 'Living in the Present', 'The Power of Now argues that focusing on the present moment is the path to spiritual enlightenment. Eckhart Tolle teaches how to quiet the mind and live fully in the now.\n\nKey teachings:\n- The pain-body\n- Ego identification\n- Presence and consciousness\n- Surrender and acceptance\n\nThe book offers practical guidance for achieving inner peace and reducing suffering through present-moment awareness.'),
            
            (66, 'Finding Meaning in Suffering', 'Man\'s Search for Meaning chronicles Viktor Frankl\'s experiences as a prisoner in Nazi concentration camps and describes his psychotherapeutic method of finding meaning in all forms of existence.\n\nKey insights:\n- Life has meaning under all circumstances\n- Our main motivation is the search for meaning\n- We have freedom to find meaning\n\nFrankl argues that we cannot avoid suffering, but we can choose how to cope with it and find meaning in it.'),
            
            (67, 'Principles of Effectiveness', 'The 7 Habits of Highly Effective People presents a principle-centered approach for solving personal and professional problems.\n\nThe seven habits:\n1. Be proactive\n2. Begin with the end in mind\n3. Put first things first\n4. Think win-win\n5. Seek first to understand, then to be understood\n6. Synergize\n7. Sharpen the saw\n\nThese habits provide a framework for personal effectiveness and character development.'),
            
            (68, 'From Good to Great', 'Good to Great examines why some companies make the leap to great results while others don\'t. Jim Collins and his team studied companies over five years.\n\nKey findings:\n- Level 5 Leadership\n- First who, then what\n- Confront the brutal facts\n- The Hedgehog Concept\n- Culture of discipline\n- Technology accelerators\n\nThe book identifies patterns that distinguish great companies from merely good ones.'),
            
            (69, 'Building Nike', 'Shoe Dog is Phil Knight\'s memoir about creating Nike. It chronicles the early days of the company, from selling shoes out of his car to building a global brand.\n\nThe story covers:\n- The partnership with his former coach\n- Struggles with cash flow and creditors\n- Competition with Adidas and Puma\n- Building a revolutionary company\n\nKnight\'s honest account reveals the challenges and triumphs of entrepreneurship.'),
            
            (70, 'Building Amazon', 'The Everything Store chronicles Amazon\'s rise from internet startup to one of the most powerful companies in the world. It provides insight into Jeff Bezos\'s vision and management.\n\nKey themes:\n- Customer obsession\n- Long-term thinking\n- Innovation and experimentation\n- Relentless growth\n\nThe book reveals how Bezos built Amazon and his ambitious plans for the company\'s future.'),
            
            (71, 'The Story of Success', 'Outliers examines what makes high-achievers different. Malcolm Gladwell argues that success is not just about individual merit but also circumstances and opportunities.\n\nKey concepts:\n- The 10,000-Hour Rule\n- Cultural legacy\n- Practical intelligence\n- Hidden advantages\n\nThe book shows how success is shaped by factors like birth date, cultural background, and historical circumstances.'),
            
            (72, 'Two Systems of Thought', 'Thinking, Fast and Slow presents a framework for understanding how we make decisions. Daniel Kahneman describes two systems of thought.\n\nSystem 1: Fast, automatic, intuitive\nSystem 2: Slow, deliberate, logical\n\nThe book explores cognitive biases and shows how understanding these systems can improve our thinking and decision-making.'),
            
            (73, 'Two Systems of Thought', 'Thinking, Fast and Slow explores the two systems that drive how we think. System 1 is fast and intuitive; System 2 is slow and analytical.\n\nKey insights:\n- Cognitive biases affect our decisions\n- Loss aversion shapes our choices\n- We overestimate our understanding\n- Prospect theory explains decision-making\n\nUnderstanding these systems helps us make better decisions and avoid common mental pitfalls.')
        ]
        
        for book_id, chapter_title, content in content_data:
            sample_content.append((book_id, 1, chapter_title, content))
        
        cursor.executemany('''
            INSERT INTO book_content (book_id, chapter_number, chapter_title, content)
            VALUES (?, ?, ?, ?)
        ''', sample_content)

