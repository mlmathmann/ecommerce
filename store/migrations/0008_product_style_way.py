# Generated by Django 4.2.1 on 2023-05-11 08:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0007_profile_country'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='style_way',
            field=models.CharField(choices=[('S', 'Standard'), ('A', 'Aristrocratic'), ('I', 'Imaginitive'), ('F', 'Futuristic'), ('B', 'Brutalistic'), ('M', 'Minimalistic')], default='S', max_length=1),
        ),
    ]
