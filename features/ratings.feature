Feature: Ratings
    As an administrator I want to be able to calculate the rating whenever a game is created or updated, and display that rating in different views

Background: Assume the user is an administrator, access control is tested elsewhere
    Given I am logged in as an admin

Scenario: Creating a game with 4 players 
    Given at least 4 players exist
      And I remember the number of rating entries for the player with id 1
     When I create a game with 4 players
     Then the number of rating entries for the player with id 1 should increase by 1

Scenario: Viewing the ratinglist after creating a game
    Given at least 4 players exist
     When I create a game of type mcr that finished at 2015-01-01T00:00
     Then the ratinglist for mcr should contain 4 players
      And the ratinglist for riichi should contain 0 players

Scenario: Winning the only game should put you at the top of the rating list
    Given at least 4 players exist
     When I create a game of type mcr where the player with id 3 won
     Then the player with id 3 should be in position 1 on the mcr ratinglist
