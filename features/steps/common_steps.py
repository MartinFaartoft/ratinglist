from behave import *
import requests
import json
from rest_framework import status
from api_helper import *

@given(u'I am logged in as an admin')
def step_impl(context):
    login(context, 'admin', 'admin')
    #assert context.response.status_code == status.HTTP_302_FOUND

@given(u'I am not logged in')
def step_impl(context):
    logout(context)

@then(u'I should be told that I am forbidden from doing that')
def step_impl(context):
    assert context.response.status_code == status.HTTP_403_FORBIDDEN

@then(u'I should be told that I am not authorized to do that')
def step_impl(context):
    assert context.response.status_code == status.HTTP_401_UNAUTHORIZED

@then(u'I should not be allowed to delete')
def step_impl(context):
    assert context.response.status_code == status.HTTP_409_CONFLICT

@when(u'I request the {game_type} ratinglist')
def step_impl(context, game_type):
    get_rating_list(context, game_type)

@then(u'I should be allowed to receive it')
def step_impl(context):
    assert context.response.status_code == status.HTTP_200_OK