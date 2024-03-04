Feature: Book Details Display
  Scenario: Viewing details of a specific book
    Given the server is running1
    When a visitor navigates to a specific book detail page with ASIN "B087D5YQXB"
    Then the book detail page should load successfully
    And the visitor should see the details of the book