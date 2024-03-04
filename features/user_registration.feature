Feature: User Registration
  Scenario: A new user registers an account
    Given the server is running8
    When a visitor registers with a username and password
    Then the user should be redirected to the login page