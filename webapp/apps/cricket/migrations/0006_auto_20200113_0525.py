# Generated by Django 2.2.7 on 2020-01-13 05:25

from django.db import migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('cricket', '0005_auto_20200112_1742'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='batting_history',
            field=jsonfield.fields.JSONField(default=dict),
        ),
        migrations.AddField(
            model_name='player',
            name='bowling_history',
            field=jsonfield.fields.JSONField(default=dict),
        ),
    ]