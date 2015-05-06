from behave import *
import requests
import json
from rest_framework import status
from api_helper import *

@given(u'I remember the number of rating entries for the player with id {player_id}')
def step_impl(context, player_id):
    context.number_of_rating_entries = len(get_rating_entries(context, int(player_id)))

@then(u'the number of rating entries for the player with id {player_id} should increase by 1')
def step_impl(context, player_id):
    assert context.number_of_rating_entries + 1 == len(get_rating_entries(context, int(player_id)))

@then(u'the ratinglist for {game_type} should contain {number} players')
def step_impl(context, game_type, number):
    assert len(get_rating_list(context, game_type)) == int(number)

@when(u'I create a game of type {game_type} where the player with id {player_id} won')
def step_impl(context, game_type, player_id):
    game = create_valid_game_dict(number_of_players = 4, game_type = game_type)
    game['game_players'][2]['score'] = 40
    game['game_players'][3]['score'] = -40
    create_game(context, game)


@then(u'the player with id {player_id} should be in position {position} on the {game_type} ratinglist')
def step_impl(context, player_id, position, game_type):
    assert get_rating_list(context, game_type)[int(position) - 1]['player_id'] == int(player_id)
