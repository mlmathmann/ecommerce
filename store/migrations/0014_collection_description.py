# Generated by Django 4.2 on 2023-05-24 10:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0013_collection'),
    ]

    operations = [
        migrations.AddField(
            model_name='collection',
            name='description',
            field=models.TextField(default='', max_length=500),
        ),
    ]
