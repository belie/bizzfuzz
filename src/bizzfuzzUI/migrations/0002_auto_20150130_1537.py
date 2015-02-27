# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bizzfuzzUI', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='funNumber',
            new_name='random_number',
        ),
        migrations.AlterField(
            model_name='user',
            name='birthdate',
            field=models.DateField(verbose_name=b'someones birthday')
        ),
    ]
