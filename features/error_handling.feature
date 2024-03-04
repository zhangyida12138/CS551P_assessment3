Feature: Error Handling
  Scenario: Handling a 404 error

    Given the server is running3
    When a visitor navigates to a non-existent page
    Then a custom 404 error page should be displayed
  Scenario: Handling a 500 error

    Given the server is running3
    When an internal server error occurs
    Then a custom 500 error page should be displayed