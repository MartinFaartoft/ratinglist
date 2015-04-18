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