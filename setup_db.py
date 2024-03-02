import csv
import sqlite3

def setup_database(cursor):
    # Drop existing tables
    cursor.execute('DROP TABLE IF EXISTS authors')
    cursor.execute('DROP TABLE IF EXISTS categories')
    cursor.execute('DROP TABLE IF EXISTS books')

    # Create tables
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS authors (
            author_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS categories (
            category_id INTEGER PRIMARY KEY AUTOINCREMENT,
            category_name TEXT UNIQUE NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS books (
          asin TEXT PRIMARY KEY,
          title TEXT NOT NULL,
          author_id INTEGER,
          imgUrl TEXT,
          productURL TEXT,
          publishedDate TEXT,
          category_id INTEGER,
          stars REAL,
          price REAL,
          isBestSeller BOOLEAN,
          isEditorsPick BOOLEAN,
          isGoodReadsChoice BOOLEAN,
          soldBy TEXT,
          FOREIGN KEY (author_id) REFERENCES authors (author_id),
          FOREIGN KEY (category_id) REFERENCES categories (category_id)
        )
    ''')

# Function to get or create author_id and return it.
def get_or_create_author_id(cursor, author_name):
    cursor.execute('SELECT author_id FROM authors WHERE name = ?', (author_name,))
    result = cursor.fetchone()
    if result:
        return result[0]
    else:
        cursor.execute('INSERT INTO authors (name) VALUES (?)', (author_name,))
        return cursor.lastrowid

# Function to get or create category_id and return it.
def get_or_create_category_id(cursor, category_name):
    cursor.execute('SELECT category_id FROM categories WHERE category_name = ?', (category_name,))
    result = cursor.fetchone()
    if result:
        return result[0]
    else:
        cursor.execute('INSERT INTO categories (category_name) VALUES (?)', (category_name,))
        return cursor.lastrowid

def import_data(cursor, csv_file_path):
    # Read the CSV file and insert the data into the tables.
    with open(csv_file_path, 'r', encoding='utf-8') as csvfile:
        csvreader = csv.DictReader(csvfile)
        count = 0  # Counter to ensure only 6000 records are imported.

        for row in csvreader:# Check if 'publishedDate' is not empty and count is less than 6000.
            if row['publishedDate'] and count < 6000:# Get or create the author_id.
                author_id = get_or_create_author_id(cursor, row['author']) # Get or create the category_id.
                category_id = get_or_create_category_id(cursor, row['category_name'])
                # Insert data into the books table.
                cursor.execute('''
                        INSERT INTO books (asin, title, author_id, imgUrl, productURL, 
                                           publishedDate, category_id, stars, price, 
                                           isBestSeller, isEditorsPick, isGoodReadsChoice, 
                                           soldBy) 
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (row['asin'], row['title'], author_id, row['imgUrl'], row['productURL'],
                          row['publishedDate'], category_id, row['stars'], row['price'],
                          row['isBestSeller'], row['isEditorsPick'], row['isGoodReadsChoice'],
                          row['soldBy']))
                count += 1

if __name__ == '__main__':
    # set csv file path and SQLite db path
    sqlite_db_path = 'CS551P_assessment3/shopping_data.db'
    csv_file_path = 'CS551P_assessment3/csv/bookdata.csv'

    # connect with SQLite db
    conn = sqlite3.connect(sqlite_db_path)
    cursor = conn.cursor()

    setup_database(cursor)
    import_data(cursor, csv_file_path)

    # Commit the changes and close the database connection.
    conn.commit()
    conn.close()
