# Generated by Django 4.2 on 2023-06-04 14:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0026_remove_category_meta_description_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='measurements',
            field=models.CharField(default='10000 x 10000 x 10000 cm', max_length=40),
        ),
    ]