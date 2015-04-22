# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_auto_20150418_1531'),
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('game_type', models.CharField(max_length=50)),
                ('date', models.DateTimeField()),
                ('number_of_winds', models.IntegerField()),
            ],
            options={
                'db_table': 'games',
            },
        ),
    ]
