# Generated by Django 4.2 on 2023-05-20 18:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0009_alter_product_style_way'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='style_way',
            field=models.CharField(choices=[('S', 'All'), ('A', 'Aristrocratic'), ('I', 'Imaginative'), ('F', 'Futuristic'), ('B', 'Brutalistic'), ('M', 'Minimalistic')], default='S', max_length=1),
        ),
        migrations.AlterField(
            model_name='order',
            name='country',
            field=models.CharField(choices=[('Deutschland', 'Germany'), ('Österreich', 'Austria'), ('Schweiz', 'Switzerland')], default='Deutschland', max_length=12),
        ),
        migrations.AlterField(
            model_name='profile',
            name='country',
            field=models.CharField(choices=[('Deutschland', 'Germany'), ('Österreich', 'Austria'), ('Schweiz', 'Switzerland')], default='Deutschland', max_length=12),
        ),
    ]
