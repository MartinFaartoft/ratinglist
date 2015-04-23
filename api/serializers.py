from django.forms import widgets
from rest_framework import serializers
from django.core.exceptions import ValidationError
from api.models import *

class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ('id', 'name')

class GamePlayerSerializer(serializers.ModelSerializer):
    #player = PlayerSerializer(read_only = True) #When this is uncommented, the serialization is nice, but deser doesn't work :(
        
    class Meta:
        model = GamePlayer
        player = serializers.PrimaryKeyRelatedField(read_only = True)
        fields = ('score', 'order', 'player')

class GameSerializer(serializers.ModelSerializer):
    game_players = GamePlayerSerializer(many = True, required = True)

    def create(self, validated_data):
        game_players = validated_data.pop('game_players')

        if len(game_players) < 4:
            raise ValidationError({
                'game_players': 'At least 4 players are required'
                })
        
        game = Game.objects.create(**validated_data)
        
        for row in game_players:
            game.game_players.add(GamePlayer(**row))
        
        return game

    class Meta:
        
        model = Game
        fields = ('id', 'game_type', 'date', 'number_of_winds', 'game_players')

