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
        
        if int(data['number_of_winds']) < 1:
            raise ValidationError({
                'number_of_winds': 'Invalid number of winds: %s, must be at least 1.' % data['number_of_winds'] 
                })

        if int(data['number_of_winds']) > 2 and data['game_type'] == RIICHI:
            raise ValidationError({
                'number_of_winds': 'Invalid number of winds: %s, must be at most 2 for riichi games.' % data['number_of_winds'] 
                })

        if int(data['number_of_winds']) > 4 and data['game_type'] == MCR:
            raise ValidationError({
                'number_of_winds': 'Invalid number of winds: %s, must be at most 2 for mcr games.' % data['number_of_winds'] 
                })


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

        if data['game_type'] == RIICHI:
            invalid_riichi_score = False
            for gp in game_players:
                if int(gp['score']) % 100 != 0:
                    invalid_riichi_score = True
                    break

            if invalid_riichi_score:
                raise ValidationError({
                    'game_players.score': 'One or more scores are not divisible by 100'
                })

        return data

    def create(self, validated_data):
        game_players = validated_data.pop('game_players')

        game = Game.objects.create(**validated_data)
        
        for row in game_players:
            game.game_players.add(GamePlayer(**row))
        
        r = RatingRepository()

        r.clear_rating_for_games_after(game)
        r.rate_unrated_games()
        
        return game

    def update(self, instance, validated_data):
        game_players = validated_data.pop('game_players')
        instance.game_players.all().delete()
        
        for row in game_players:
            instance.game_players.add(GamePlayer(**row))
        
        r = RatingRepository()
        r.clear_rating_for_games_after(instance)

        instance.game_type = validated_data.get('game_type', instance.game_type)
        instance.finished_time = validated_data.get('finished_time', instance.finished_time)
        instance.number_of_winds = validated_data.get('number_of_winds', instance.number_of_winds)
        instance.is_rated = False
        instance.save()

        r.clear_rating_for_games_after(instance)
        
        r.rate_unrated_games()

        return instance

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

class RatingEntryGameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ('id', 'finished_time')

class RatingEntrySerializer(serializers.ModelSerializer):
    finished_time = serializers.DateTimeField(source='game.finished_time')
    class Meta:
        model = RatingEntry
        fields = ('difficulty', 'expected_score', 'score', 'score_sum', 'rating_delta', 'rating', 'game', 'finished_time')

class RatingListSerializer(serializers.Serializer):
    rating = serializers.FloatField()
    name = serializers.CharField()
    position = serializers.IntegerField()
    player_id = serializers.IntegerField()
    score_sum = serializers.IntegerField()