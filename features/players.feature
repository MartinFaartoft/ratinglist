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

Scenario: Deleting a player with games played

Scenario: Updating a player

Scenario: Getting a list of players

Scenario: Getting a player by ID