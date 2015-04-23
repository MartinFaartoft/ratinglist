from django.db import models

class CaseInsensitiveCharField(models.CharField):
    def db_type(self, connection):
        return 'citext'

class Player(models.Model):
    name = CaseInsensitiveCharField(max_length=100, unique=True)

    class Meta:
        ordering = ('name', )
        db_table = 'players'

class Game(models.Model):
    game_type = models.CharField(max_length=50)
    date = models.DateTimeField()
    number_of_winds = models.IntegerField()

    class Meta:
        #ordering = ('game_number', )
        db_table = 'games'

class GamePlayer(models.Model):
    game = models.ForeignKey(Game, related_name='game_players')
    player = models.ForeignKey(Player)
    score = models.IntegerField()
    order = models.IntegerField()

    class Meta:
        unique_together = ("game", "player")
        db_table = 'game_players'