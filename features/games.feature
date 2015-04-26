Feature: Games
    As an administrator I want to be able to create / update / delete games so they reflect actual games played.

Background: Assume the user is an administrator, access control is tested elsewhere
    Given I am logged in as an admin

Scenario: Creating a game with 4 players    
    Given at least 4 players exist
      And I remember the number of games
     When I create a new game with 4 players
     Then the number of games should increase by 1
      And the game should contain 4 players

Scenario: Creating a game with 3 players
    Given at least 3 players exist
     When I create a new game with 3 players
     Then the game should not be created

Scenario: Creating a game with 8 players
    Given at least 8 players exist
     When I create a new game with 8 players
     Then the game should not be created

Scenario: Creating a game where the scores do not sum to zero
    Given at least 4 players exist
     When I create a new game with 4 players with scores that do not sum to zero
     Then the game should not be created

Scenario: A player is in the game more than once
    Given at least 4 players exist
     When I create a new game with 4 players where one player is duplicated
     Then the game should not be created

Scenario: A player that does not exist is in the game
    Given at least 4 players exist
     When I create a new game with 4 players where one player does not exist
     Then the game should not be created

Scenario: A new game should have a position
    Given at least 4 players exist
      And no games exist
     When I create a new valid game
     Then the game should have a position of 1

Scenario: The list of games should be sorted by position descending
    Given at least 4 players exist
      And no games exist
     When I create a new valid game
      And I create a new valid game
     Then the first game in the list should have position 2

Scenario: A riichi game has a score that is not evenly divisible by 100

Scenario: The order of the players in a game is wrong

Scenario: The gametype is invalid

Scenario: The number of winds is invalid