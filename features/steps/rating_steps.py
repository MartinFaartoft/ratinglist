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