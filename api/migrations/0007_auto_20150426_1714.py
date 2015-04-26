# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_auto_20150423_2027'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='position',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='game',
            unique_together=set([('game_type', 'position')]),
        ),
    ]
