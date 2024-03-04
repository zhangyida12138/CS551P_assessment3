Feature: User Logout
  Scenario: A logged-in user logs out
    Given a user is logged in
    When the user logs out
    Then the user should be logged out successfully