Feature: Ratings
    As an administrator I want to be able to calculate the rating whenever a game is created or updated, and display that rating in different views

Background: Assume the user is an administrator, access control is tested elsewhere
    Given I am logged in as an admin

Scenario: Creating a game with 4 players 
    Given at least 4 players exist
      And I remember the number of rating entries for the player with id 1
     When I create a game with 4 players
     Then the number of rating entries for the player with id 1 should increase by 1