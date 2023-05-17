from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from store.models import *
from store.forms import *


@login_required(login_url='loginpage')
def profile(request, user):
    user_email = User.objects.filter(username=user).values('email')
    if user_email:
        for email in user_email:
            user_email = email.get('email')
    else:
        user_email = ''
    user_phone = Profile.objects.filter(user=request.user).values('phone')
    if user_phone:
        for phone in user_phone:
            user_phone = phone.get('phone')
    else:
        user_phone = ''
    user_street = Profile.objects.filter(user=request.user).values('street')
    if user_street:
        for street in user_street:
            user_street = street.get('street')
    else:
        user_street = ''
    user_house_number = Profile.objects.filter(user=request.user).values('house_number')
    if user_house_number:
        for house_number in user_house_number:
            user_house_number = house_number.get('house_number')
    else:
        user_house_number = ''
    user_address_info = Profile.objects.filter(user=request.user).values('address_info')
    if user_address_info:
        for address_info in user_address_info:
            user_address_info = address_info.get('address_info')
    else:
        user_address_info = ''
    user_postal_code = Profile.objects.filter(user=request.user).values('postal_code')
    if user_postal_code:
        for postal_code in user_postal_code:
            user_postal_code = postal_code.get('postal_code')
    else:
        user_postal_code = ''
    user_city = Profile.objects.filter(user=request.user).values('city')
    if user_city:
        for city in user_city:
            user_city = city.get('city')
    else:
        user_city = ''
    user_country = Profile.objects.filter(user=request.user).values('country')
    if user_country:
        for country in user_country:
            user_country = country.get('country')
    else:
        user_country = ''
    user_time = Profile.objects.filter(user=request.user).values('created_at')
    if user_time:
        for time in user_time:
            user_time = time.get('created_at')
    else:
        user_time = ''
        # TODO: Ausgabe auf deutsch und nur das Datum/ Jahr
    context = {'user': user,
               'user_email': user_email,
               'user_phone': user_phone,
               'user_street': user_street,
               'user_house_number': user_house_number,
               'user_address_info': user_address_info,
               'user_postal_code': user_postal_code,
               'user_city': user_city,
               'user_country': user_country,
               'user_time': user_time}
    return render(request, "store/profile.html", context)


@login_required(login_url='loginpage')
def details(request, user):
    user_email = User.objects.filter(username=user).values('email')
    user_fname = User.objects.filter(username=user).values('first_name')
    user_lname = User.objects.filter(username=user).values('last_name')
    if user_fname:
        for name in user_fname:
            user_fname = name.get('first_name')
    else:
        user_fname = ''
    if user_lname:
        for name in user_lname:
            user_lname = name.get('last_name')
    else:
        user_lname = ''
    if user_email:
        for email in user_email:
            user_email = email.get('email')
    else:
        user_email = ''
    user_phone = Profile.objects.filter(user=request.user).values('phone')
    if user_phone:
        for phone in user_phone:
            user_phone = phone.get('phone')
    else:
        user_phone = ''
    user_street = Profile.objects.filter(user=request.user).values('street')
    if user_street:
        for street in user_street:
            user_street = street.get('street')
    else:
        user_street = ''
    user_house_number = Profile.objects.filter(user=request.user).values('house_number')
    if user_house_number:
        for house_number in user_house_number:
            user_house_number = house_number.get('house_number')
    else:
        user_house_number = ''
    user_address_info = Profile.objects.filter(user=request.user).values('address_info')
    if user_address_info:
        for address_info in user_address_info:
            user_address_info = address_info.get('address_info')
    else:
        user_address_info = ''
    user_postal_code = Profile.objects.filter(user=request.user).values('postal_code')
    if user_postal_code:
        for postal_code in user_postal_code:
            user_postal_code = postal_code.get('postal_code')
    else:
        user_postal_code = ''
    user_city = Profile.objects.filter(user=request.user).values('city')
    if user_city:
        for city in user_city:
            user_city = city.get('city')
    else:
        user_city = ''
    user_country = Profile.objects.filter(user=request.user).values('country')
    if user_country:
        for country in user_country:
            user_country = country.get('country')
    else:
        user_country = ''
    context = {'user': user,
               'user_fname': user_fname,
               'user_lname': user_lname,
               'user_email': user_email,
               'user_phone': user_phone,
               'user_street': user_street,
               'user_house_number': user_house_number,
               'user_address_info': user_address_info,
               'user_postal_code': user_postal_code,
               'user_city': user_city,
               'user_country': user_country}
    return render(request, "store/details.html", context)
