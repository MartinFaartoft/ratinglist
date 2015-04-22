# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_game'),
    ]

    operations = [
        migrations.CreateModel(
            name='GamePlayer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('score', models.IntegerField()),
                ('order', models.IntegerField()),
                ('game', models.ForeignKey(to='api.Game')),
                ('player', models.ForeignKey(to='api.Player')),
            ],
            options={
                'db_table': 'game_players',
            },
        ),
    ]
