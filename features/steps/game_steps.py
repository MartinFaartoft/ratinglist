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

@then(u'the game should not be updated')
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
    for game in context.response.json():
        assert game['game_type'] == game_type

@then(u'I should not receive a list of games')
def step_impl(context):
    assert context.response.status_code == status.HTTP_404_NOT_FOUND

@given(u'I remember the id of the new game')
@when(u'I remember the id of the new game')
def step_impl(context):
    context.new_game_id = context.response.json()['id']

@when(u'I delete the remembered game')
def step_impl(context):
    delete_game(context, context.new_game_id)

@then(u'the game should be deleted')
def step_impl(context):
    assert context.response.status_code == status.HTTP_204_NO_CONTENT
    assert context.client.get(base_url + '/games/%s/' % context.new_game_id).status_code == status.HTTP_404_NOT_FOUND

@when(u'I update the remembered game by changing the gametype to {game_type} and the number of winds to {number}')
def step_impl(context, game_type, number):
    game = flatten_game(context.game)
    game['game_type'] = game_type
    if number:
        game['number_of_winds'] = number
    update_game(context, game)

@then(u'the remembered game should have gametype {game_type}')
def step_impl(context, game_type):
    assert get_game(context, context.new_game_id)['game_type'] == game_type

@when(u'I update the remembered game by adding player {player_id} with {score} points')
def step_impl(context, player_id, score):
    game = flatten_game(context.game)
    game['game_players'].append(dict(player = player_id, score = score, order = len(game['game_players']) + 1))
    update_game(context, game)

@then(u'the remembered game should have {number} players')
def step_impl(context, number):
    assert len(get_game(context, context.new_game_id)['game_players']) == int(number)

@when(u'I update the remembered game by changing the {field} to {value}')
def step_impl(context, field, value):
    game = flatten_game(context.game)
    game[field] = value
    update_game(context, game)

@then(u'the remembered game should have {field} equal to {value}')
def step_impl(context, field, value):
    game = get_game(context, context.new_game_id)
    print(game[field])
    print(value)
    assert game[field] == value
