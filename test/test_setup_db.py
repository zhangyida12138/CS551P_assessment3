import unittest
import sqlite3
import os
import sys

# Add the parent directory to sys.path to be able to import the setup_db module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import setup_db

class DatabaseTest(unittest.TestCase):
    """Test case for the database setup and data import."""

    def setUp(self):
        """Setup a test database before each test."""
        self.db_path = 'test_shopping_data.db'
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()

        # Run the database setup script to create tables
        setup_db.setup_database(self.cursor)

    def tearDown(self):
        """Destroy the test database after each test."""
        self.conn.close()
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def test_tables_created(self):
        """Test whether the tables are created successfully."""
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = {row[0] for row in self.cursor.fetchall()}
        
        # We expect to see three tables: authors, categories, and books
        expected_tables = {'authors', 'categories', 'books'}
        self.assertTrue(expected_tables.issubset(tables))

    def test_data_imported(self):
        """Test whether the data is imported successfully into the books table."""
        csv_file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'csv/bookdata.csv')
        setup_db.import_data(self.cursor, csv_file_path)

        # Assert that the books table is not empty
        self.cursor.execute("SELECT * FROM books")
        books_data = self.cursor.fetchall()
        self.assertGreater(len(books_data), 0)

        # Assert that no more than 6000 records are imported
        self.assertLessEqual(len(books_data), 6000)

if __name__ == '__main__':
    unittest.main()
