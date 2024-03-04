Feature: Database setup and data import
   Scenario: Successfully set up database and imported data
     Given has created an empty SQLite database
     When executing database creation and data import scripts
     Then the database should contain the correct table structure
     Then should successfully import the specified number of records into each table