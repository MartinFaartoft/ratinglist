# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_auto_20150426_1714'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='game',
            options={'ordering': ('-finished_time',)},
        ),
        migrations.RenameField(
            model_name='game',
            old_name='date',
            new_name='finished_time',
        ),
        migrations.AlterUniqueTogether(
            name='game',
            unique_together=set([('game_type', 'finished_time')]),
        ),
        migrations.RemoveField(
            model_name='game',
            name='position',
        ),
    ]
