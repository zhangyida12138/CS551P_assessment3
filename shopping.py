from flask import Flask, render_template, g,request,redirect, url_for
import sqlite3 
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

# Initialize a new Flask application instance.
app = Flask(__name__)
app.secret_key = 'secret_key'
# Define a constant for the database file path.
DATABASE = 'shopping_data.db'


# Function to get a database connection.
# This will be used to connect to the SQLite database.
def get_db_connection():
    db = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row
    return db


# Register a function to be called when the application context ends.
# When the Flask app context is destroyed, this function will close the database connection.
@app.teardown_appcontext
def close_connection(exception):
  # Get the database connection from `g` if it exists.
    db = getattr(g, '_database', None)
    if db is not None:
      # Close the database connection.
        db.close()


# Define the route for the root URL ('/').
@app.route('/')
def index():
    conn = None  # Initialize the connection variable.
    try:
        
        # Get a database connection and create a cursor to execute SQL commands.
        conn = get_db_connection()
        app.logger.info('Index page is accessed.')
        cursor = conn.cursor()
        app.logger.info('Index page is accessed.')
        # Execute a SQL query to retrieve books marked as bestsellers.
        # Join the 'books' table with the 'authors' table to get the author's name.
        cursor.execute('''
            SELECT b.asin, b.title, a.name as author, b.imgUrl, b.productURL, b.price
            FROM books b
            JOIN authors a ON b.author_id = a.author_id
            ORDER BY RANDOM()
            LIMIT 40;
        ''')
        app.logger.info('Index page is accessed.')
        # Fetch all the results of the query.
        featured_books = cursor.fetchall()
        app.logger.info(f"Number of books fetched: {len(featured_books)}")
        # for book in featured_books:
        #     print(book['title'], book['author'], book['price'])  # Example of printing title, author, and price.
        #     # Use app.logger.info if you prefer logging instead of printing.
        #     app.logger.info(f"Book: {book['title']}, Author: {book['author']}, Price: {book['price']}")

        app.logger.info('Index page is accessed.')
        # Render the 'index.html' template, passing the featured books as a context variable.
        return render_template('index.html', featured_books=featured_books)
    except sqlite3.DatabaseError as error:
        # If a database error occurs, print it to the console and return an error response.
        print(f"Database error: {error}")
        return "A database error occurred.", 500
    finally:
        # Ensure the database connection is closed whether or not an error occurred.
        if conn:
            conn.close()

@app.route('/books')
def book_list():
    conn = get_db_connection()
    cursor = conn.cursor()
    # Query all book information and get the author name and category name at the same time
    cursor.execute('''
        SELECT b.asin, b.title, b.imgUrl, b.productURL, b.price, a.name as author
        FROM books b
        JOIN authors a ON b.author_id = a.author_id
    ''')
    books = cursor.fetchall()
    conn.close()
    return render_template('book_list.html', books=books)

@app.route('/book/<asin>')
def book_detail(asin):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT b.asin, b.title, a.name as author, b.imgUrl, b.productURL, 
               b.price, b.stars, b.publishedDate, 
               b.isBestSeller, b.isEditorsPick, b.isGoodReadsChoice
        FROM books b
        JOIN authors a ON b.author_id = a.author_id
        WHERE b.asin = ?
    ''', (asin,))
    book = cursor.fetchone()
    conn.close()
    
    if book:
        # Convert book data into a dictionary for easy access by name in the template
        book_dict = {
            'asin': book['asin'],
            'title': book['title'],
            'author': book['author'],
            'imgUrl': book['imgUrl'],
            'productURL': book['productURL'],
            'price': book['price'],
            'stars': book['stars'],
            'publishedDate': book['publishedDate'],
            'isBestSeller': book['isBestSeller'],
            'isEditorsPick': book['isEditorsPick'],
            'isGoodReadsChoice': book['isGoodReadsChoice']
        }
        return render_template('book_detail.html', book=book_dict)
    else:
        return "Can not found the book", 404

@app.route('/search')
def search():
    query = request.args.get('query', '')  # Get search keywords from URL query parameters
    conn = get_db_connection()
    books = []
    app.logger.info('db is connected.')
    if query:
        # Execute search query
        cursor = conn.cursor()
        cursor.execute('''
            SELECT b.asin, b.title, b.imgUrl, b.productURL, b.price, a.name as author,
                   c.category_name, b.stars, b.publishedDate, b.isBestSeller, 
                   b.isEditorsPick, b.isGoodReadsChoice
            FROM books b
            JOIN authors a ON b.author_id = a.author_id
            JOIN categories c ON b.category_id = c.category_id
            WHERE b.title LIKE ? OR a.name LIKE ? OR c.category_name LIKE ?
            ORDER BY b.title ASC;
        ''', ('%' + query + '%', '%' + query + '%', '%' + query + '%'))
        books = cursor.fetchall()
        app.logger.info('search.')
    conn.close()
    return render_template('search_results.html', search_results=books, query=query)

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE id = ?", (int(user_id),))
        user_record = cursor.fetchone()
        if user_record:
            user = UserMixin()
            user.id = user_record['id']  # Flask-Login 要求用户对象有一个 id 属性
            return user
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
    return None

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # 加密密码
        password_hash = generate_password_hash(password)
        
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password_hash))
            conn.commit()
        except sqlite3.IntegrityError:  # 捕获用户名重复的异常
            return "Username already taken", 400
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        user_record = cursor.fetchone()
        
        if user_record and check_password_hash(user_record['password'], password):
            user = UserMixin()
            user.id = user_record['id']
            login_user(user)
            return redirect(url_for('index'))
        else:
            return "Invalid username or password", 401
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/secret')
@login_required
def secret():
    return "Only authenticated users can see this."

# errorhandler
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    app.logger.error(f"server error: {e}, path: {request.url}")
    return render_template('500.html'), 500

@app.errorhandler(Exception)
def handle_exception(e):
    app.logger.error(f"unhandled exception: {e}, path: {request.url}")
    return render_template('error.html', error=e), 500

if __name__ == '__main__':
    app.run(debug=True)   