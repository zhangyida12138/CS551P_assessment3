Feature: Search for Books
  Scenario: Searching for books with a keyword
    Given the server is running5
    When a visitor searches for a keyword
    Then the search results should display all books matching the keyword