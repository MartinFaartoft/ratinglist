from django.forms import widgets
from rest_framework import serializers
from api.models import *

class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ('id', 'name')

class GamePlayerSerializer(serializers.ModelSerializer):
        
    class Meta:
        model = GamePlayer
        player = serializers.PrimaryKeyRelatedField(read_only = True)
        fields = ('score', 'order', 'player')

class GameSerializer(serializers.ModelSerializer):
    game_players = GamePlayerSerializer(many = True, required = True)

    def create(self, validated_data):
        game_players = validated_data.pop('game_players')
        
        game = Game.objects.create(**validated_data)
        
        for row in game_players:
            game.game_players.add(GamePlayer(**row))
        
        return game

    class Meta:
        
        model = Game
        fields = ('id', 'game_type', 'date', 'number_of_winds', 'game_players')

