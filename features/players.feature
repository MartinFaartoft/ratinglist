Feature: Player Maintenance
	As an administrator, I want to be able to maintain a list of players

Scenario: Creating a player
	Given I am logged in as an admin
	  And I count the number of players
	 When I create a new player with the name "Test"
	 Then The number of players should increase by one

Scenario: Duplicate player names
    Given I am logged in as an admin
      And I count the number of players
     When I create a new player with the name "Test"
      And I create a new player with the name "Test"
     Then The number of players should increase by one

Scenario: Duplicate player names with different casing
    Given I am logged in as an admin
      And I count the number of players
     When I create a new player with the name "test"
      And I create a new player with the name "TEST"
     Then The number of players should increase by one

Scenario: Deleting a player with no games played
    Given I am logged in as an admin
      And a player with id 1 exists
      And the player with id 1 has not played any games
     When I delete the player with id 1
     Then a player with id 1 should not exist

Scenario: Deleting a player with games played
    Given I am logged in as an admin
      And a player with id 1 exists
     When I create a new game with 4 players
      And I delete the player with id 1
     Then I should not be allowed to delete
      And a player with id 1 should exist

Scenario: Updating a player
    Given I am logged in as an admin
      And a player with id 1 exists
     When I update the player with id 1 to have the name NewName
      And I retrieve the player with id 1
     Then the player should have the name NewName

Scenario: Getting a player by id
    Given a player with id 1 exists
     When I retrieve the player with id 1
     Then the player should have a name that is not empty
