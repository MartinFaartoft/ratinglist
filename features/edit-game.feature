Feature: Edit Game
    As an administrator I want to be able to edit games so they reflect actual games played, and have the ratinglist be up to date at all times

Background: Assume the user is an administrator, access control is tested elsewhere
    Given I am logged in as an admin

Scenario: Changing the gametype
    Given I create a riichi game with 2 winds that finished at 2015-01-01T00:00 where the player with id 3 got 100 points
      And I remember the id of the new game
     When I update the remembered game by changing the gametype to mcr
     Then the remembered game should have gametype mcr

Scenario: Replacing a player
    Given I create a riichi game with 2 winds that finished at 2015-01-01T00:00 where the player with id 3 got 100 points
      And I remember the id of the new game
     When I update the remembered game by adding player 5 with 0 points
     Then the remembered game should have 5 players
