# Generated by Django 4.2 on 2023-06-01 09:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0025_alter_collection_description_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='meta_description',
        ),
        migrations.RemoveField(
            model_name='category',
            name='meta_keywords',
        ),
        migrations.RemoveField(
            model_name='category',
            name='meta_title',
        ),
        migrations.RemoveField(
            model_name='product',
            name='meta_description',
        ),
        migrations.RemoveField(
            model_name='product',
            name='meta_keywords',
        ),
        migrations.RemoveField(
            model_name='product',
            name='meta_title',
        ),
        migrations.RemoveField(
            model_name='product',
            name='original_price',
        ),
        migrations.RemoveField(
            model_name='product',
            name='tag',
        ),
    ]
