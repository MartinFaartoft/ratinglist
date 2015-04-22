from behave import *
import requests
from rest_framework import status

base_url = 'http://localhost:8000'

def login(context, username, password):
    url = base_url + '/auth/login'
    login_data = dict(username=username, password=password)
    context.response = context.client.post(url, data=login_data)
    #if context.response.status_code == 200:
        #context.client.headers['X-CSRFToken'] = context.client.cookies['csrftoken']

def logout(context):
    url = base_url + '/auth/logout'
    context.response = context.client.post(url)

def get_players(context):
    context.response = context.client.get(base_url + '/players/')
    return context.response.json()

def create_player(context, name):
    url = base_url + '/players/'
    context.response = context.client.post(url, data = dict(name = name))

def get_games(context):
    context.response = context.client.get(base_url + '/games/')
    return context.response.json()

def create_game(context, game):
    context.response = context.client.post(base_url + '/games/', data = game)
    return context.response.json()

@given(u'I am logged in as an admin')
def step_impl(context):
    login(context, 'admin', 'admin')
    assert context.response.status_code == status.HTTP_302_FOUND

@given(u'I count the number of players')
def step_impl(context):
    players = get_players(context)
    context.player_count = len(players)

@when(u'I create a new player with the name "{name}"')
def step_impl(context, name):
    create_player(context, name)

@then(u'The number of players should increase by one')
def step_impl(context):
    players = get_players(context)
    assert context.player_count + 1 == len(players)

@given(u'at least {number} players exist')
def step_impl(context, number):
    n = int(number)
    assert len(get_players(context)) >= n

@given(u'I remember the number of games')
def step_impl(context):
    games = get_games(context)
    context.game_count = len(games)

@when(u'I create a new game with 4 players')
def step_impl(context):
    game = dict()
    game['game_type'] = 'mcr'
    game['number_of_winds'] = 4
    game['date'] = '2015-04-22T00:00'

    game_players = []
    game_players.append(dict(player_id = 1, score = 0, order = 0))
    game_players.append(dict(player_id = 2, score = 0, order = 1))
    game_players.append(dict(player_id = 3, score = 0, order = 2))
    game_players.append(dict(player_id = 4, score = 0, order = 3))
    game['game_players'] = game_players
    print(game)
    context.created_game = create_game(context, game)


@then(u'the number of games should increase by 1')
def step_impl(context):
    assert context.game_count + 1 == len(get_games(context))

@then(u'the game should contain {number} players')
def step_impl(context, number):
    n = int(number)
    assert n == len(context.created_game.game_players)