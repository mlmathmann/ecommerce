# Generated by Django 4.2 on 2023-06-04 18:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0030_billingaddress_email'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='billing_address',
        ),
        migrations.AddField(
            model_name='order',
            name='bill_address_dif',
            field=models.BooleanField(default=False, help_text='0=default, 1=Different Billing Address given'),
        ),
        migrations.AddField(
            model_name='order',
            name='bill_address_info',
            field=models.TextField(max_length=150, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='bill_city',
            field=models.CharField(max_length=150, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='bill_country',
            field=models.CharField(choices=[('Deutschland', 'Germany'), ('Österreich', 'Austria'), ('Schweiz', 'Switzerland')], max_length=12, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='bill_email',
            field=models.CharField(max_length=150, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='bill_fname',
            field=models.CharField(max_length=150, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='bill_house_number',
            field=models.CharField(max_length=150, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='bill_lname',
            field=models.CharField(max_length=150, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='bill_phone',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='bill_postal_code',
            field=models.CharField(max_length=150, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='bill_street',
            field=models.CharField(max_length=150, null=True),
        ),
    ]
