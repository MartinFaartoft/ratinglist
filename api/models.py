from django.db import models

class Player(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ('name', )
        db_table = 'players'