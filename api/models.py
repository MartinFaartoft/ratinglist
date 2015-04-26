from django.db import models
from django.db import connection

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
    position = models.IntegerField()

    class Meta:
        ordering = ('-position', )
        unique_together = ('game_type', 'position')
        db_table = 'games'

    def save(self, *args, **kwargs):
        #assume for now that games are always added to the end of the 'list'
        cursor = connection.cursor()
        cursor.execute('SELECT MAX(position) FROM games WHERE game_type = %s', [self.game_type])
        position = cursor.fetchone()[0]
        if position is not None:
            self.position = int(position) + 1
        else:
            self.position = 1
        print('POSITION', self.position)
        super(Game, self).save()

class GamePlayer(models.Model):
    game = models.ForeignKey(Game, related_name='game_players')
    player = models.ForeignKey(Player)
    score = models.IntegerField()
    order = models.IntegerField()

    class Meta:
        unique_together = ('game', 'player')
        db_table = 'game_players'