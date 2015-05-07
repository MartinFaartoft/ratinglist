Feature: Games
    As an administrator I want to be able to create / update / delete games so they reflect actual games played.

Background: Assume the user is an administrator, access control is tested elsewhere
    Given I am logged in as an admin

Scenario: Creating a game with 4 players    
    Given at least 4 players exist
      And I remember the number of games
     When I create a game with 4 players
     Then the number of games should increase by 1
      And the game should contain 4 players

Scenario: Creating a game with 3 players
    Given at least 3 players exist
     When I create a game with 3 players
     Then the game should not be created

Scenario: Creating a game with 8 players
    Given at least 8 players exist
     When I create a game with 8 players
     Then the game should not be created

Scenario: Creating a game where the scores do not sum to zero
    Given at least 4 players exist
     When I create a game with 4 players with scores that do not sum to zero
     Then the game should not be created

Scenario: A player is in the game more than once
    Given at least 4 players exist
     When I create a game with 4 players where one player is duplicated
     Then the game should not be created

Scenario: A player that does not exist is in the game
    Given at least 4 players exist
     When I create a game with 4 players where one player does not exist
     Then the game should not be created

Scenario: Two games of the same type are finished at the same time
    Given at least 4 players exist
     When I create a game of type mcr that finished at 2015-01-01T00:00
      And I create a game of type mcr that finished at 2015-01-01T00:00
     Then the game should not be created

Scenario: Two games of different types are finished at the same time
    Given at least 4 players exist
     When I create a game of type mcr that finished at 2015-01-01T00:00
      And I create a game of type riichi that finished at 2015-01-01T00:00
     Then the game should be created

Scenario: The gametype is invalid
    Given at least 4 players exist
     When I create a game of type invalidgametype that finished at 2015-01-01T00:00
     Then the game should not be created

Scenario: Requesting a list of mcr games
     When I create a game of type mcr that finished at 2015-01-01T00:00
      And I create a game of type riichi that finished at 2015-01-01T00:00
     When I request the list of mcr games
     Then I should receive a list of mcr games

Scenario: Requesting a list of riichi games
     When I create a game of type mcr that finished at 2015-01-01T00:00
      And I create a game of type riichi that finished at 2015-01-01T00:00
     When I request the list of riichi games
     Then I should receive a list of riichi games

Scenario: Requesting a list of games of an invalid game type
     When I request the list of invalidgametype games
     Then I should not receive a list of games

Scenario: The number of winds in a riichi game is greater than 2
     When I create a riichi game with 3 winds
     Then the game should not be created

Scenario: The number of winds in a riichi game is less than 1
    When I create a riichi game with 0 winds
    Then the game should not be created

Scenario: The number of winds in a mcr game is greater than 4
     When I create a mcr game with 5 winds
     Then the game should not be created

Scenario: The number of winds in a mcr game is less than 1
     When I create a mcr game with 0 winds
     Then the game should not be created

Scenario: Deleting a game
     When I create a game with 4 players
      And remember the id of the new game
      And delete the new game
     Then the game should be deleted


Scenario: The game finished in the future

Scenario: The list of games should be sorted by finished_time
    
Scenario: A riichi game has a score that is not evenly divisible by 100

Scenario: The order of the players in a game is wrong
