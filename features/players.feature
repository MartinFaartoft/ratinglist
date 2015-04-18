Feature: Player Maintenance
	As an administrator, I want to be able to maintain a list of players

Scenario: Creating a player
	Given I am logged in as an admin
	  And no players exist
	 When I create a new player
	 Then The number of players should be 1

Scenario: Duplicate player names
    Given I am logged in as an admin
      And no players exist
     When I create a new player with the name "Test"
      And I create a new player with the name "Test"
     Then The number of players should be 1

Scenario: Deleting a player with no games played

Scenario: Deleting a player with games played

Scenario: Updating a player

Scenario: Getting a list of players

Scenario: Getting a player by ID