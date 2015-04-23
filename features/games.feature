Feature: Games
    As an administrator I want to be able to create / update / delete games so they reflect actual games played.

Scenario: Creating a game with 4 players
    Given I am logged in as an admin
      And at least 4 players exist
      And I remember the number of games
     When I create a new game with 4 players
     Then the number of games should increase by 1
      And the game should contain 4 players

Scenario: Creating a game with 3 players
    Given I am logged in as an admin
      And at least 3 players exist
     When I create a new game with 3 players
     Then the game should not be created
