from django.forms import widgets
from rest_framework import serializers
ValidationError = serializers.ValidationError
from api.models import *
from game_rater import *

class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ('id', 'name')

class GamePlayerSerializer(serializers.ModelSerializer):
    #player = PlayerSerializer(read_only = True) #When this is uncommented, the serialization is nice, but deser doesn't work :(
        
    class Meta:
        model = GamePlayer
        fields = ('score', 'order', 'player')

class GameCreateSerializer(serializers.ModelSerializer):
    game_players = GamePlayerSerializer(many = True, required = True)

    def validate(self, data):
        """Single field validation is done on Django model instances, this method takes care of multi-field validation"""
        game_players = data['game_players']

        if len(game_players) < 4:
            raise ValidationError({
                'game_players': 'At least 4 players are required'
                })

        if len(game_players) > 7:
            raise ValidationError({
                'game_players': 'No more than 7 players allowed'
                })

        score_sum = sum(map(lambda x: int(x['score']), game_players))
        if score_sum != 0:
            raise ValidationError({
                'game_players.score': 'Score does not sum to zero'
                })

        unique_player_ids = set(map(lambda x: x['player'], game_players))
        if len(unique_player_ids) < len(game_players):
            raise ValidationError({
                'game_players.player': 'Duplicate players are not allowed'
                })

        return data

    def create(self, validated_data):
        game_players = validated_data.pop('game_players')

        game = Game.objects.create(**validated_data)
        
        for row in game_players:
            game.game_players.add(GamePlayer(**row))
        
        rate_game(game)

        return game

    class Meta:        
        model = Game
        fields = ('id', 'game_type', 'finished_time', 'number_of_winds', 'game_players')


class GamePlayerViewSerializer(serializers.ModelSerializer):
    player = PlayerSerializer(read_only = True)
        
    class Meta:
        model = GamePlayer
        fields = ('score', 'order', 'player')

class GameViewSerializer(serializers.ModelSerializer):
    game_players = GamePlayerViewSerializer(many = True)

    class Meta:
        model = Game
        fields = ('id', 'game_type', 'finished_time', 'number_of_winds', 'game_players')

class RatingEntrySerializer(serializers.ModelSerializer):

    class Meta:
        model = RatingEntry
        fields = ('difficulty', 'expected_score', 'score', 'score_sum', 'rating_delta', 'rating', 'game')