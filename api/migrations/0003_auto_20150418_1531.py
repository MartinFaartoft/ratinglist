# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import api.models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20150418_1516'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='name',
            field=api.models.CaseInsensitiveCharField(unique=True, max_length=100),
        ),
    ]
