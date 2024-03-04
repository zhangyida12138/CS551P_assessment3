Kindle Book Shopping Website README
Overview
This project is a web-based shopping platform for Kindle books, allowing users to browse, search, and purchase books through Amazon. It supports features like user registration and login, but guests can also browse the website without registering. The website is developed with Flask, using SQLite for database management, and is designed with a base interface that all other pages inherit from.

Features
User Authentication: Users can choose to register or login to access personalized features. However, browsing the website is possible without registration.
Book Recommendations: The index page features a random recommendation of 40 books for users to explore.
Book Listing: Users can view a comprehensive list of all available books on the booklist page.
Search Functionality: A search option is available on the top-right corner of every page, allowing users to find books by title or author.
Book Details: Each book is presented in a card format, with an option to view more details. The detail page includes a button to purchase the book from Amazon.
Responsive Design: All pages are developed from a base interface, ensuring a unified and responsive design across the website.
Technical Details
Backend: The website is powered by Flask, with SQLite used for database management. shopping.py handles routing, while setup_db.py is used for database setup.
Database Structure: The database (shopping_data.db) consists of tables for authors, categories, books, and users. Book information is imported from CSV files, while user information is stored upon registration.
Frontend: HTML pages are stored in the templates folder, with corresponding CSS files in the static folder. Original data is kept in the csv folder.
Testing: Behavior testing is conducted with files in the feature folder, testing various user interactions and website functionality.
Database Schema
Authors: Stores author names with unique IDs.
Categories: Stores unique category names with IDs.
Books: Contains detailed information about each book, including relationships to authors and categories.
Users: Stores user information, including usernames and hashed passwords.
Security
Flask-Login: Used for handling user authentication sessions.
Werkzeug.security: Ensures data security, particularly for user passwords.
Setup and Installation
Ensure Python and Flask are installed on your system.
Clone the repository to your local machine.
Run setup_db.py to initialize the database.
Start the Flask server by executing shopping.py.
Access the website through the provided local URL.
Contribution
This project is developed as part of the CS551P course assessment 2. Contributions and feedback are welcome to improve the website's functionality and user experience.

Note
This README is designed to offer a comprehensive overview of the Kindle Book Shopping Website project. For detailed instructions on setup and configuration, refer to the individual script files and comments within the codebase.