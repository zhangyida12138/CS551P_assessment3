Feature: User Login
  Scenario: A registered user logs in
    Given the server is running6
    And a user has already registered
    When the user logs in with correct credentials
    Then the user should be logged in successfully
    And redirected to the home page1