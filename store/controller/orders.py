import json

from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from store.models import Order, OrderItem, Profile, GeneratedItem, Creation
from store.views import get_navbar_context


@login_required(login_url='loginpage')
def orders_index(request):
    nav_context = get_navbar_context(request)
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    items_list = []

    for order in orders:
        order_items = OrderItem.objects.filter(order__tracking_no=order.tracking_no)
        items_list.append(order_items)

    context = {'orders': orders, 'items_list': items_list, 'categories': nav_context.get('categories'), 'profile_picture': nav_context.get('profile_picture'), 'collections': nav_context.get('collections')}
    return render(request, 'store/orders/myordersview.html', context)


def orders_view(request, order):
    nav_context = get_navbar_context(request)
    order = Order.objects.filter(tracking_no=order).first()
    order_items = OrderItem.objects.filter(order=order)
    userprofile = Profile.objects.filter(user=request.user).first()

    user_country = Profile.objects.filter(user=request.user).values('country')

    if user_country:
        for country in user_country:
            user_country = country.get('country')
            for choice in Order.CountryChoices.choices:
                if user_country == choice[1].lower():
                    user_country = choice[1].lower()
    else:
        user_country = ''


    context = {'order': order, 'order_items': order_items,'categories': nav_context.get('categories'),
               'profile_picture': nav_context.get('profile_picture'), 'collections': nav_context.get('collections'),
               'userprofile': userprofile, 'user_country': user_country}
    return render(request, 'store/orders/myordersdetails.html', context)


def furniture_index(request):
    nav_context = get_navbar_context(request)
    creations = Creation.objects.filter(user=request.user).order_by('-created_at')
    items_list = []

    for creation in creations:
        gen_item = GeneratedItem.objects.filter(creation__tracking_no=creation.tracking_no)
        items_list.append(gen_item)

    context = {'creations': creations, 'items_list': items_list, 'categories': nav_context.get('categories'),
               'profile_picture': nav_context.get('profile_picture'), 'collections': nav_context.get('collections')}
    return render(request, 'store/orders/myfurniture.html', context)


def furniture_view(request, creation_tracking_no):
    nav_context = get_navbar_context(request)
    creation = Creation.objects.filter(tracking_no=creation_tracking_no).first()
    prompt = creation.order.prompt
    promp_json = json.loads(prompt.replace("'", '"'))
    style = promp_json.get('style')
    object = promp_json.get('objekt')
    material = promp_json.get('material')
    creation_prompt = f'A {style} {object} made out of {material}'

    version = creation.version
    # object-position: 0% 0%; - 1
    # object-position: 100% 0%; - 2
    # object-position: 0% 100%; - 3
    # object-position: 100% 100%; - 4


    context = {'creation': creation, 'categories': nav_context.get('categories'),
               'profile_picture': nav_context.get('profile_picture'), 'collections': nav_context.get('collections'),
               'creation_prompt': creation_prompt}
    return render(request, 'store/orders/myfurnituredetails.html', context)

