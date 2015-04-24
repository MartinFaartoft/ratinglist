Feature: Access Control
    As a site owner, I want to limit access to POST, PUT and DELETE calls to protect data integrity

Scenario: Creating a player without being logged in
    Given I am not logged in
     When I create a new player with the name "Test"
     Then I should be told that I am forbidden from doing that

