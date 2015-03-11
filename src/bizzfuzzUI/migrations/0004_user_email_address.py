# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bizzfuzzUI', '0003_auto_20150302_1406'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='email_address',
            field=models.CharField(max_length=255, null=True, blank=True),
            preserve_default=True,
        ),
    ]
