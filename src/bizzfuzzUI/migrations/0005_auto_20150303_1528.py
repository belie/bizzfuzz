# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bizzfuzzUI', '0004_user_email_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='forgot_password_code',
            field=models.CharField(max_length=255, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='user',
            name='forgot_password_date',
            field=models.DateTimeField(null=True, verbose_name=b'The date someone initiates the password request'),
            preserve_default=True,
        ),
    ]
