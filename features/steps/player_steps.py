from behave import *
import requests
import json
from rest_framework import status
from api_helper import *

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


@given(u'a player with id {player_id} exists')
@then(u'a player with id {player_id} should exist')
def step_impl(context, player_id):
    assert get_player(context, player_id) is not None

@given(u'the player with id {player_id} has not played any games')
def step_impl(context, player_id):
    assert len(get_games(context)) == 0

@when(u'I delete the player with id {player_id}')
def step_impl(context, player_id):
    delete_player(context, player_id)

@then(u'a player with id {player_id} should not exist')
def step_impl(context, player_id):
    assert get_player(context, player_id) is None

@when(u'I update the player with id {player_id} to have the name {name}')
def step_impl(context, player_id, name):
    update_player(context, player_id, name)

@when(u'I retrieve the player with id {player_id}')
def step_impl(context, player_id):
    context.player = get_player(context, player_id)

@then(u'the player should have the name {name}')
def step_impl(context, name):
    assert context.player['name'] == name

@then(u'the player should have a name that is not empty')
def step_impl(context):
    assert len(context.player['name']) > 0