from django.db import models
from django.db import connection

RIICHI = 'riichi'
MCR = 'mcr'

class CaseInsensitiveCharField(models.CharField):
    def db_type(self, connection):
        return 'citext'

class Player(models.Model):
    name = CaseInsensitiveCharField(max_length=100, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('name', )
        db_table = 'players'

class Game(models.Model):
    VALID_GAME_TYPES = ((MCR, MCR), (RIICHI, RIICHI))
    game_type = models.CharField(max_length=50, choices=VALID_GAME_TYPES)
    finished_time = models.DateTimeField()
    number_of_winds = models.IntegerField()
    is_rated = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-finished_time', )
        unique_together = ('game_type', 'finished_time')
        db_table = 'games'

class GamePlayer(models.Model):
    game = models.ForeignKey(Game, related_name='game_players')
    player = models.ForeignKey(Player)
    score = models.IntegerField()
    order = models.IntegerField()

    class Meta:
        unique_together = ('game', 'player')
        db_table = 'game_players'

class RatingEntry(models.Model):
    game = models.ForeignKey(Game)
    player = models.ForeignKey(Player, related_name='rating_entries')
    difficulty = models.FloatField()
    expected_score = models.FloatField()
    score = models.IntegerField()
    score_sum = models.IntegerField()
    rating_delta = models.FloatField()
    rating = models.FloatField()

    class Meta:
        ordering = ('-game__finished_time', )
        unique_together = ('game', 'player')
        db_table = 'rating_entries'