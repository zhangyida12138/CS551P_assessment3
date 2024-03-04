Feature: visit index
  Scenario: Visiting the home page
    Given the server is running10
    When a visitor navigates to the home page
    Then the home page should load successfully
    And a list of featured books should be displayed