from django.db import models

class CaseInsensitiveCharField(models.CharField):
    def db_type(self, connection):
        return 'citext'

class Player(models.Model):
    name = CaseInsensitiveCharField(max_length=100, unique=True)

    class Meta:
        ordering = ('name', )
        db_table = 'players'