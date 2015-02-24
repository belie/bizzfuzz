# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('birthdate', models.DateField(verbose_name=b"someone's birthday")),
                ('funNumber', models.IntegerField(verbose_name=b'bizzbuzz randomly generated number')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
