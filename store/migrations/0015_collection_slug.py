# Generated by Django 4.2 on 2023-05-24 16:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0014_collection_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='collection',
            name='slug',
            field=models.CharField(default='', max_length=150),
        ),
    ]
