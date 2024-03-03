from flask import Flask, render_template, g,request
import sqlite3 

# Initialize a new Flask application instance.
app = Flask(__name__)

# Define a constant for the database file path.
DATABASE = 'shopping_data.db'


# Function to get a database connection.
# This will be used to connect to the SQLite database.
def get_db_connection():
    # Check if there's already a database connection in the global object `g`.
    # If not, establish a new database connection and store it in `g`.
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        # Configure the connection to return rows that behave like dictionaries.
        # This allows accessing the columns of a row by name.
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


if __name__ == '__main__':
    app.run(debug=True)   