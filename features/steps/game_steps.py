from behave import *
import requests
import json
from rest_framework import status
from api_helper import *

@given(u'I remember the number of games')
def step_impl(context):
    games = get_games(context)
    context.game_count = len(games)

@when(u'I create a game with {number} players')
def step_impl(context, number):
    game = create_valid_game_dict(int(number))
    context.created_game = create_game(context, game)

@when(u'I create a game with {number} players with scores that do not sum to zero')
def step_impl(context, number):
    game = create_valid_game_dict(int(number))
    game['game_players'][0]['score'] = 10
    create_game(context, game)    

@when(u'I create a game with {number} players where one player is duplicated')
def step_impl(context, number):
    game = create_valid_game_dict(int(number))
    game['game_players'][1]['player'] = 1
    create_game(context, game)

@when(u'I create a game with {number} players where one player does not exist')
def step_impl(context, number):
    game = create_valid_game_dict(int(number))
    game['game_players'][1]['player'] = 1337
    create_game(context, game)

@when(u'I create a game of type {game_type} that finished at {datetime}')
def step_impl(context, game_type, datetime):
    game = create_valid_game_dict(4, game_type, datetime)
    context.created_game = create_game(context, game)

@then(u'the number of games should increase by 1')
def step_impl(context):
    assert context.game_count + 1 == len(get_games(context))

@then(u'the game should contain {number} players')
def step_impl(context, number):
    n = int(number)
    assert n == len(context.created_game['game_players'])

@then(u'the game should not be created')
def step_impl(context):
    assert context.response.status_code == status.HTTP_400_BAD_REQUEST

@then(u'the game should be created')
def step_impl(context):
    assert context.response.status_code == status.HTTP_201_CREATED

@given(u'no games exist')
def step_impl(context):
    assert len(get_games(context)) == 0

@when(u'I create a new valid game')
def step_impl(context):
    context.created_game = create_game(context, create_valid_game_dict(4))

@when(u'I request the list of {game_type} games')
def step_impl(context, game_type):
    context.response = context.client.get(base_url + '/games/' + game_type + '/')

@when(u'I create a {game_type} game with {number_of_winds} winds')
def step_impl(context, game_type, number_of_winds):
    game = create_valid_game_dict(game_type = game_type)
    game['number_of_winds'] = int(number_of_winds)
    create_game(context, game)

@then(u'I should receive a list of {game_type} games')
def step_impl(context, game_type):
    assert context.response.status_code == status.HTTP_200_OK
    assert context.response.json()[0]['game_type'] == game_type

@then(u'I should not receive a list of games')
def step_impl(context):
    assert context.response.status_code == status.HTTP_404_NOT_FOUND