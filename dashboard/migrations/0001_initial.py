# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='RecommendStocks',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('symbol', models.CharField(max_length=45)),
                ('name', models.TextField(blank=True)),
                ('exchange', models.CharField(max_length=45, blank=True)),
                ('sector', models.CharField(max_length=45, blank=True)),
            ],
            options={
                'db_table': 'recommend_stocks',
            },
            bases=(models.Model,),
        ),
    ]
