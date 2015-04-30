# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_auto_20150430_0938'),
    ]

    operations = [
        migrations.CreateModel(
            name='RatingEntry',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('difficulty', models.FloatField()),
                ('expected_score', models.FloatField()),
                ('score', models.IntegerField()),
                ('score_sum', models.IntegerField()),
                ('rating_delta', models.FloatField()),
                ('rating', models.FloatField()),
                ('game', models.ForeignKey(to='api.Game')),
                ('player', models.ForeignKey(related_name='rating_entries', to='api.Player')),
            ],
            options={
                'db_table': 'rating_entries',
            },
        ),
        migrations.AlterUniqueTogether(
            name='ratingentry',
            unique_together=set([('game', 'player')]),
        ),
    ]
