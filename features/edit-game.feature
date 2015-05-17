Feature: Edit Game
    As an administrator I want to be able to edit games so they reflect actual games played, and have the ratinglist be up to date at all times

Background: Assume the user is an administrator, access control is tested elsewhere
    Given I am logged in as an admin

Scenario: Changing the gametype
    Given I create a riichi game with 2 winds that finished at 2015-01-01T00:00 where the player with id 3 got 100 points
      And I remember the id of the new game
     When I update the remembered game by changing the gametype to mcr and the number of winds to 2
     Then the remembered game should have gametype mcr

Scenario: Replacing a player
    Given I create a riichi game with 2 winds that finished at 2015-01-01T00:00 where the player with id 3 got 100 points
      And I remember the id of the new game
     When I update the remembered game by adding player 5 with 0 points
     Then the remembered game should have 5 players

Scenario: Changing the finished time
    Given I create a riichi game with 2 winds that finished at 2015-01-01T00:00 where the player with id 3 got 100 points
      And I remember the id of the new game
     When I update the remembered game by changing the finished_time to 2015-01-02T00:00:00Z
     Then the remembered game should have finished_time equal to 2015-01-02T00:00:00Z

Scenario: Invalid number of winds in update
    Given I create a riichi game with 2 winds that finished at 2015-01-01T00:00 where the player with id 3 got 100 points
      And I remember the id of the new game
     When I update the remembered game by changing the number_of_winds to 5
     Then the game should not be updated

Scenario: Rating should be recalculated after updating a game
    Given I create a riichi game with 2 winds that finished at 2015-01-01T00:00 where the player with id 3 got 100 points
      And I remember the id of the new game
      And I create a riichi game with 2 winds that finished at 2015-01-02T00:00 where the player with id 3 got 100 points
     Then the player with id 3 should have 4.818 in riichi rating 
      And the player with id 3 should not have any mcr rating 
     When I update the remembered game by changing the gametype to mcr and the number of winds to 4
     Then the player with id 3 should have 2.439 in mcr rating 
      And the player with id 3 should have 2.439 in riichi rating 
     
