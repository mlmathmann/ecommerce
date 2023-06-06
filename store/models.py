from django.db import models
import datetime
import os
from django.contrib.auth.forms import User


# Create your models here. The table structure for the database is defined here.

# sets the file path of each uploaded image to the uploads directory
def get_file_path(request, filename):
    original_filename = filename
    nowTime = datetime.datetime.now().strftime('%Y%m%d%H:%M:%S')
    filename = "%s%s" % (nowTime, original_filename)
    return os.path.join('uploads/', filename)


# sets the file path of each creation image to the uploads/generated directory
def generated_file_path(request, filename):
    return os.path.join('uploads/generated/', filename)


class Category(models.Model):
    slug = models.CharField(max_length=150, null=False, blank=False)
    name = models.CharField(max_length=150, null=False, blank=False)
    image = models.ImageField(upload_to=get_file_path, null=True, blank=True)
    description = models.TextField(max_length=500, null=False, blank=False)
    status = models.BooleanField(default=False, help_text="0=default, 1=Hidden")
    trending = models.BooleanField(default=False, help_text="0=default, 1=Trending")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Collection(models.Model):
    name = models.CharField(max_length=150, null=False, blank=False)
    slug = models.CharField(max_length=150, null=False, blank=False, default='')
    style_sign = models.CharField(max_length=1, null=False, blank=False, default='')
    image = models.ImageField(upload_to=get_file_path, null=True, blank=True)
    description = models.TextField(max_length=1000, null=False, blank=False, default='')

    def __str__(self):
        return self.name


class Product(models.Model):
    class StyleChoices(models.TextChoices):
        ARISTROCRATIC = 'A'
        IMAGINATIVE = 'I'
        FUTURISTIC = 'F'
        BRUTALISTIC = 'B'
        SIMPLISTIC = 'S'

    slug = models.CharField(max_length=150, null=False, blank=False)
    name = models.CharField(max_length=150, null=False, blank=False)
    product_image = models.ImageField(upload_to=get_file_path, null=True, blank=True)
    small_description = models.CharField(max_length=250, null=False, blank=False)
    quantity = models.IntegerField(null=False, blank=False)
    description = models.TextField(max_length=1000, null=False, blank=False)
    selling_price = models.FloatField(null=False, blank=False)
    status = models.BooleanField(default=False, help_text="0=default, 1=Hidden")
    trending = models.BooleanField(default=False, help_text="0=default, 1=Trending")
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    style_way = models.CharField(max_length=1, choices=StyleChoices.choices, default='S')
    measurements = models.CharField(max_length=40, null=False, blank=False, default='10000 x 10000 x 10000 cm')



    def __str__(self):
        return self.name


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    product_quantity = models.IntegerField(null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)


class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class Profile(models.Model):
    class StyleChoices(models.TextChoices):
        ALL = 'S'
        ARISTROCRATIC = 'A'
        IMAGINATIVE = 'I'
        FUTURISTIC = 'F'
        BRUTALISTIC = 'B'
        MINIMALISTIC = 'M'

    class CountryChoices(models.TextChoices):
        germany = "Deutschland"
        austria = "Österreich"
        switzerland = "Schweiz"

    style_way = models.CharField(max_length=1, choices=StyleChoices.choices, default='S')
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(null=True, blank=True, upload_to=get_file_path)
    phone = models.CharField(max_length=50, null=False)
    street = models.CharField(max_length=150, null=False)
    house_number = models.CharField(max_length=150, null=False)
    address_info = models.TextField(max_length=150, null=True)
    postal_code = models.CharField(max_length=150, null=False)
    city = models.CharField(max_length=150, null=False)
    country = models.CharField(max_length=12, choices=CountryChoices.choices, default='Deutschland')
    newsletter_subscription = models.BooleanField(default=False, help_text="0=default, 1=Subscribed")
    created_at = models.DateTimeField(auto_now_add=True)


class BillingAddress(models.Model):
    class CountryChoices(models.TextChoices):
        germany = "Deutschland"
        austria = "Österreich"
        switzerland = "Schweiz"

    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    fname = models.CharField(max_length=150, null=False, default='')
    lname = models.CharField(max_length=150, null=False, default='')
    email = models.CharField(max_length=150, null=False, default='')
    phone = models.CharField(max_length=50, null=False)
    street = models.CharField(max_length=150, null=False)
    house_number = models.CharField(max_length=150, null=False)
    address_info = models.TextField(max_length=150, null=True)
    postal_code = models.CharField(max_length=150, null=False)
    city = models.CharField(max_length=150, null=False)
    country = models.CharField(max_length=12, choices=CountryChoices.choices)
    created_at = models.DateTimeField(auto_now_add=True)


class Order(models.Model):
    class CountryChoices(models.TextChoices):
        germany = "Deutschland"
        austria = "Österreich"
        switzerland = "Schweiz"

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    fname = models.CharField(max_length=150, null=False)
    lname = models.CharField(max_length=150, null=False)
    email = models.CharField(max_length=150, null=False)
    phone = models.CharField(max_length=50, null=False)
    street = models.CharField(max_length=150, null=False)
    house_number = models.CharField(max_length=150, null=False)
    address_info = models.TextField(max_length=150, null=True)
    postal_code = models.CharField(max_length=150, null=False)
    city = models.CharField(max_length=150, null=False)
    country = models.CharField(max_length=12, choices=CountryChoices.choices, default='Deutschland')

    bill_address_dif = models.BooleanField(default=False, help_text="0=default, 1=Different Billing Address given")

    bill_fname = models.CharField(max_length=150, null=True)
    bill_lname = models.CharField(max_length=150, null=True)
    bill_email = models.CharField(max_length=150, null=True)
    bill_phone = models.CharField(max_length=50, null=True)
    bill_street = models.CharField(max_length=150, null=True)
    bill_house_number = models.CharField(max_length=150, null=True)
    bill_address_info = models.TextField(max_length=150, null=True)
    bill_postal_code = models.CharField(max_length=150, null=True)
    bill_city = models.CharField(max_length=150, null=True)
    bill_country = models.CharField(max_length=12, choices=CountryChoices.choices, null=True)

    total_price = models.FloatField(null=False)
    payment_mode = models.CharField(max_length=150, null=False)
    payment_id = models.CharField(max_length=250, null=True)
    order_statuses = (
        ('Pending', 'Pending'),
        ('Out on delivery', 'Out on delivery'),
        ('Completed', 'Completed')
    )
    status = models.CharField(max_length=150, choices=order_statuses, default='Pending')
    message = models.TextField(null=True)
    tracking_no = models.CharField(max_length=150, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{} - {}'.format(self.id, self.tracking_no)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.FloatField(null=False)
    quantity = models.IntegerField(null=False)

    def __str__(self):
        return '{} {}'.format(self.order.id, self.order.tracking_no)


class GeneratedItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=generated_file_path, null=False, blank=False)
    prompt = models.CharField(max_length=150, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)


class Creation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.CharField(max_length=150, null=False)
    order = models.ForeignKey(GeneratedItem, on_delete=models.CASCADE)
    version = models.CharField(max_length=1, null=False)

    creation_statuses = (
        ('Requested', 'Requested'),
        ('Approved', 'Approved'),
        ('In production', 'In production'),
        ('Out on delivery', 'Out on delivery'),
        ('Completed', 'Completed')
    )
    status = models.CharField(max_length=150, choices=creation_statuses, default='Requested')
    message = models.TextField(null=True)
    tracking_no = models.CharField(max_length=150, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{} - {}'.format(self.id, self.tracking_no)

