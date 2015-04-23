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
        player = serializers.PrimaryKeyRelatedField(queryset = Player.objects)
        fields = ('score', 'order', 'player')


class GameSerializer(serializers.ModelSerializer):
    game_players = GamePlayerSerializer(many = True, required = True)

    def create(self, validated_data):
        game = Game()
        game.number_of_winds = validated_data['number_of_winds']
        game.date = validated_data['date']
        game.game_type = validated_data['game_type']
        game.save()
        
        for row in validated_data['game_players']:
            gp = GamePlayer()
            gp.score = row['score']
            gp.order = row['order']
            
            gp.player = row['player']
            game.game_players.add(gp)
        
        return Game.objects.get(pk=game.pk)

    class Meta:
        
        model = Game
        fields = ('id', 'game_type', 'date', 'number_of_winds', 'game_players')

