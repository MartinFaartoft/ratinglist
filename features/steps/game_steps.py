from behave import *
import requests
import json
from rest_framework import status
from api_helper import *

@given(u'I remember the number of games')
def step_impl(context):
    games = get_games(context)
    context.game_count = len(games)

@when(u'I create a new game with {number} players')
def step_impl(context, number):
    game = create_valid_game_dict(int(number))
    context.created_game = create_game(context, game)

@when(u'I create a new game with {number} players with scores that do not sum to zero')
def step_impl(context, number):
    game = create_valid_game_dict(int(number))
    game['game_players'][0]['score'] = 10
    create_game(context, game)    

@when(u'I create a new game with {number} players where one player is duplicated')
def step_impl(context, number):
    game = create_valid_game_dict(int(number))
    game['game_players'][1]['player'] = 1
    create_game(context, game)

@when(u'I create a new game with {number} players where one player does not exist')
def step_impl(context, number):
    game = create_valid_game_dict(int(number))
    game['game_players'][1]['player'] = 1337
    create_game(context, game)

@then(u'the number of games should increase by 1')
def step_impl(context):
    assert context.game_count + 1 == len(get_games(context))

@then(u'the game should contain {number} players')
def step_impl(context, number):
    n = int(number)
    assert n == len(context.created_game['game_players'])

@then(u'the game should not be created')
def step_impl(context):
    print(context.response.status_code)
    assert context.response.status_code == status.HTTP_400_BAD_REQUEST #!= status.HTTP_201_CREATED

@given(u'no games exist')
def step_impl(context):
    assert len(get_games(context)) == 0

@when(u'I create a new valid game')
def step_impl(context):
    context.created_game = create_game(context, create_valid_game_dict(4))

@then(u'the game should have a position of 1')
def step_impl(context):
    assert context.created_game['position'] == 1

@then(u'the first game in the list should have position 2')
def step_impl(context):
    assert get_games(context)[0]['position'] == 2