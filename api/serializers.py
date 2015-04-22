from django.forms import widgets
from rest_framework import serializers
from api.models import *

class GamePlayerSerializer(serializers.ModelSerializer):
    class Meta:
        #player = PlayerSerializer(source='player_id')
        #game = GameSerializer(source='game_id')
        model = GamePlayer
        fields = ('score', 'order')

class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ('id', 'name')

class GameSerializer(serializers.ModelSerializer):
    class Meta:
        game_players = GamePlayerSerializer(many=True, read_only = True)
        model = Game
        fields = ('id', 'game_type', 'date', 'number_of_winds', 'game_players')

