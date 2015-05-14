from features.steps.api_helper import *
import requests

class Context():
    client = requests.session()

context = Context()
login(context, 'admin', 'admin')

for i in range(8):
    create_player(context, 'Test %s' % i)