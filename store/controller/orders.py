from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from store.models import Order, OrderItem, Profile
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
    pass


def furniture_view(request, furniture):
    pass


def requestfurniture(request):
    print(request.user)                     # user
    print()                                 # die generierten items nach user filtern und neustes holen siehe oben
    print(request.POST.get('selected'))     # version
    print(request.POST.get('email'))        # email, kann auch auto complete sein
    print(request.POST.get('message'))      # ist optional

    return render(request, "store/midjourney.html")