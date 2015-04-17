from django.db import models

class Player(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        ordering = ('name', )
        db_table = 'players'