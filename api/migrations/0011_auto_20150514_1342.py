# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_auto_20150507_1000'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2015, 5, 14, 13, 42, 33, 640112, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='game',
            name='modified',
            field=models.DateTimeField(default=datetime.datetime(2015, 5, 14, 13, 42, 39, 640018, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='player',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2015, 5, 14, 13, 42, 46, 256144, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='player',
            name='modified',
            field=models.DateTimeField(default=datetime.datetime(2015, 5, 14, 13, 42, 54, 104471, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
    ]
