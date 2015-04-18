from behave import *
import requests
from requests.auth import HTTPBasicAuth

base_url = 'http://localhost:8000'

def login(context, username, password):
    context.auth = HTTPBasicAuth(username, password)

def logout(context):
    url = base_url + '/api-auth/logout'
    context.response = context.client.post(url)

@given(u'I am logged in as an admin')
def step_impl(context):
    login(context, 'admin', 'admin')

@given(u'no players exist')
def step_impl(context):
    context.response = context.client.get(base_url + '/players/', auth=context.auth)
    assert len(context.response.json()) == int(0)