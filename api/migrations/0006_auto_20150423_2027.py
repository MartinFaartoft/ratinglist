# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_gameplayer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gameplayer',
            name='game',
            field=models.ForeignKey(related_name='game_players', to='api.Game'),
        ),
        migrations.AlterUniqueTogether(
            name='gameplayer',
            unique_together=set([('game', 'player')]),
        ),
    ]
