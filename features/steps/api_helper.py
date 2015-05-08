import requests
import json
from rest_framework import status

base_url = 'http://localhost:8000'

def login(context, username, password):
    url = base_url + '/api-token-auth/'
    login_data = dict(username=username, password=password)
    context.response = context.client.post(url, data=login_data)
    if context.response.status_code == status.HTTP_200_OK:
        context.client.headers['Authorization'] = 'JWT ' + context.response.json()['token']
        print(context.client.headers)

def logout(context):
    if 'Authorization' in context.client.headers:
        del context.client.headers['Authorization']
    
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

def delete_game(context, new_game_id):
    context.response = context.client.delete(base_url + '/games/%s/' % new_game_id)

def create_valid_game_dict(number_of_players = 4, game_type = 'mcr', finished_time = '2015-04-22T00:00'):
    n = number_of_players

    game = dict()
    game['game_type'] = game_type
    game['number_of_winds'] = 1
    game['finished_time'] = finished_time

    game_players = []
    for i in range(n):
        game_players.append(dict(player = i+1, score = 0, order = i))
    game['game_players'] = game_players

    return game

def delete_player(context, id):
    context.response = context.client.delete(base_url + '/players/' + id)

def get_rating_entries(context, player_id, game_type):
    context.response = context.client.get(base_url + '/players/%s/rating/%s/' % (player_id, game_type))
    return context.response.json()

def get_rating_list(context, game_type):
    context.response = context.client.get(base_url + '/ratinglist/%s/' % game_type)
    return context.response.json()