Feature: Book List Display
  Scenario: Viewing the list of books
    Given the server is running2
    When a visitor navigates to the book list page
    Then the book list page should load successfully