# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_auto_20150430_1209'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ratingentry',
            options={'ordering': ('-game__finished_time',)},
        ),
        migrations.AddField(
            model_name='game',
            name='is_rated',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='game',
            name='game_type',
            field=models.CharField(max_length=50, choices=[(b'mcr', b'mcr'), (b'riichi', b'riichi')]),
        ),
    ]
