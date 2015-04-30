import requests
import json
from rest_framework import status

base_url = 'http://localhost:8000'

def login(context, username, password):
    context.client.auth = (username, password)
    #url = base_url + '/auth/login'
    #login_data = dict(username=username, password=password)
    #context.response = context.client.post(url, data=login_data)
    #assert context.response.status_code == status.HTTP_302_FOUND
    #if context.response.status_code == 200:
        #context.client.headers['X-CSRFToken'] = context.client.cookies['csrftoken']

def logout(context):
    url = base_url + '/auth/logout'
    context.response = context.client.post(url)

def get_players(context):
    context.response = context.client.get(base_url + '/players/')
    return context.response.json()

def get_player(context, player_id):
    context.response = context.client.get(base_url + '/players/' + player_id)
    if context.response.status_code == status.HTTP_200_OK:
        return context.response.json()
    return

def create_player(context, name):
    url = base_url + '/players/'
    context.response = context.client.post(url, data = dict(name = name))

def update_player(context, player_id, name):
    url = base_url + '/players/' + player_id
    context.response = context.client.put(url, data = dict(name = name))

def get_games(context):
    context.response = context.client.get(base_url + '/games/')
    return context.response.json()

def create_game(context, game):
    headers = {'Content-type': 'application/json'}
    game_json = json.dumps(game)
    #print(game_json)
    context.response = context.client.post(base_url + '/games/', data = game_json, headers=headers)

    try:
        return context.response.json()
    except:
        return

def create_valid_game_dict(number_of_players):
    n = number_of_players

    game = dict()
    game['game_type'] = 'mcr'
    game['number_of_winds'] = 4
    game['finished_time'] = '2015-04-22T00:00'

    game_players = []
    for i in range(n):
        game_players.append(dict(player = i+1, score = 0, order = i))
    game['game_players'] = game_players

    return game

def delete_player(context, id):
    context.response = context.client.delete(base_url + '/players/' + id)
