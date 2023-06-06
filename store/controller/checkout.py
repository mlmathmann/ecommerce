import sweetify
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from store.models import Cart, Order, OrderItem, Product, Profile, BillingAddress
from store.views import get_navbar_context
from django.http import JsonResponse
import random


# general checkout page, displays the users profile info such as address and name if given, lists the products in the cart
# with the total price
@login_required(login_url='loginpage')
def index(request):
    nav_context = get_navbar_context(request)
    rawcart = Cart.objects.filter(user=request.user)
    cart_item_count = Cart.objects.filter(user=request.user).count()

    if cart_item_count == 0:
        new_total_price = None

    for item in rawcart:
        if item.product_quantity > item.product.quantity:
            Cart.objects.delete(id=item.id)

    cartitems = Cart.objects.filter(user=request.user)
    total_price = 0
    for item in cartitems:
        total_price = total_price + item.product.selling_price * item.product_quantity
        format_str = '{{:,.{}f}}'.format(2)
        number_str = format_str.format(total_price)
        new_total_price = number_str.replace(',', 'X').replace('.', ',').replace('X', '.')
    total_price = "{:.2f}".format(total_price)

    userprofile = Profile.objects.filter(user=request.user).first()

    billing_address = BillingAddress.objects.filter(profile__user=request.user).first()

    user_country = Profile.objects.filter(user=request.user).values('country')

    if user_country:
        for country in user_country:
            user_country = country.get('country')
            for choice in Order.CountryChoices.choices:
                if user_country == choice[1].lower():
                    user_country = choice[1].lower()
    else:
        user_country = ''

    billing_country = BillingAddress.objects.filter(profile__user=request.user).values('country')

    if billing_country:
        for country in billing_country:
            billing_country = country.get('country')
            for choice in Order.CountryChoices.choices:
                if billing_country == choice[0]:
                    billing_country = choice[1].lower()

    else:
        billing_country = ''

    context = {'cartitems': cartitems,
               'cart_item_count': cart_item_count,
               'total_price': new_total_price,
               'total_price_calc': total_price,
               'userprofile': userprofile,
               'user_country': user_country,
               'billing_address': billing_address,
               'billing_country': billing_country,
               'categories': nav_context.get('categories'),
               'profile_picture': nav_context.get('profile_picture'),
               'collections': nav_context.get('collections')
               }
    return render(request, 'store/checkout.html', context)


# places the customers order, gets the entered address and payment information as well as the products and their quantity,
# removes the quantity from the stock
@login_required(login_url='loginpage')
def placeorder(request):
    if request.method == 'POST':

        currentuser = User.objects.filter(id=request.user.id).first()

        if not currentuser.first_name:
            currentuser.first_name = request.POST.get('fname')
            currentuser.last_name = request.POST.get('lname')
            currentuser.save()
        else:
            if request.POST.get('fname') != '':
                if request.POST.get('fname') != currentuser.__getattribute__('first_name'):
                    currentuser.first_name = request.POST.get('fname')
                    currentuser.save()

            if request.POST.get('lname') != '':
                if request.POST.get('lname') != currentuser.__getattribute__('last_name'):
                    currentuser.last_name = request.POST.get('lname')
                    currentuser.save()

        if not Profile.objects.filter(user=request.user):
            userprofile = Profile()
            userprofile.user = request.user
            userprofile.email = request.POST.get('email')
            userprofile.phone = request.POST.get('phone')
            userprofile.street = request.POST.get('street')
            userprofile.house_number = request.POST.get('house_number')
            userprofile.address_info = request.POST.get('address_info')
            userprofile.postal_code = request.POST.get('postal_code')
            userprofile.city = request.POST.get('city')
            userprofile.country = request.POST.get('country')
            userprofile.save()

            if request.POST.get('check_box') != 'true':
                billing_address = BillingAddress()
                billing_address.profile = userprofile
                billing_address.fname = request.POST.get('bill_fname')
                billing_address.lname = request.POST.get('bill_lname')
                billing_address.email = request.POST.get('bill_email')
                billing_address.phone = request.POST.get('bill_phone')
                billing_address.street = request.POST.get('bill_street')
                billing_address.house_number = request.POST.get('bill_house_number')
                billing_address.address_info = request.POST.get('bill_address_info')
                billing_address.postal_code = request.POST.get('bill_postal_code')
                billing_address.city = request.POST.get('bill_city')
                billing_address.country = request.POST.get('bill_country')
                billing_address.save()

        else:
            profile_obj = Profile.objects.filter(user=request.user)
            if request.POST.get('phone') != '':
                for element in profile_obj.values('phone'):
                    if request.POST.get('phone') != element.get('phone'):
                        profile_obj.update(phone=request.POST.get('phone'))

            if request.POST.get('street') != '':
                for element in profile_obj.values('street'):
                    if request.POST.get('street') != element.get('street'):
                        profile_obj.update(street=request.POST.get('street'))

            if request.POST.get('house_number') != '':
                for element in profile_obj.values('house_number'):
                    if request.POST.get('house_number') != element.get('house_number'):
                        profile_obj.update(house_number=request.POST.get('house_number'))

            if request.POST.get('address_info') != '':
                for element in profile_obj.values('address_info'):
                    if request.POST.get('address_info') != element.get('address_info'):
                        profile_obj.update(address_info=request.POST.get('address_info'))

            if request.POST.get('postal_code') != '':
                for element in profile_obj.values('postal_code'):
                    if request.POST.get('postal_code') != element.get('postal_code'):
                        profile_obj.update(postal_code=request.POST.get('postal_code'))

            if request.POST.get('city') != '':
                for element in profile_obj.values('city'):
                    if request.POST.get('city') != element.get('city'):
                        profile_obj.update(city=request.POST.get('city'))

            if request.POST.get('country') != '':
                for element in profile_obj.values('country'):
                    if request.POST.get('country') != element.get('country'):
                        profile_obj.update(country=request.POST.get('country'))

            if request.POST.get('check_box') == 'true' and BillingAddress.objects.filter(profile__user=request.user):
                billing_address_obj = BillingAddress.objects.filter(profile__user=request.user).first()
                billing_address_obj.delete()

            elif request.POST.get('check_box') == '' and BillingAddress.objects.filter(profile__user=request.user).first() is None:
                billing_address = BillingAddress()
                billing_address.profile = profile_obj.first()
                billing_address.fname = request.POST.get('bill_fname')
                billing_address.lname = request.POST.get('bill_lname')
                billing_address.email = request.POST.get('bill_email')
                billing_address.phone = request.POST.get('bill_phone')
                billing_address.street = request.POST.get('bill_street')
                billing_address.house_number = request.POST.get('bill_house_number')
                billing_address.address_info = request.POST.get('bill_address_info')
                billing_address.postal_code = request.POST.get('bill_postal_code')
                billing_address.city = request.POST.get('bill_city')
                billing_address.country = request.POST.get('bill_country')
                billing_address.save()
            else:
                billing_address_obj = BillingAddress.objects.filter(profile__user=request.user)
                if request.POST.get('bill_fname') != '':
                    for element in billing_address_obj.values('fname'):
                        if request.POST.get('bill_fname') != element.get('fname'):
                            billing_address_obj.update(fname=request.POST.get('bill_fname'))

                if request.POST.get('bill_lname') != '':
                    for element in billing_address_obj.values('lname'):
                        if request.POST.get('bill_lname') != element.get('lname'):
                            billing_address_obj.update(lname=request.POST.get('bill_lname'))

                if request.POST.get('bill_email') != '':
                    for element in billing_address_obj.values('email'):
                        if request.POST.get('bill_email') != element.get('email'):
                            billing_address_obj.update(email=request.POST.get('bill_email'))

                if request.POST.get('bill_phone') != '':
                    for element in billing_address_obj.values('phone'):
                        if request.POST.get('bill_phone') != element.get('phone'):
                            billing_address_obj.update(phone=request.POST.get('bill_phone'))

                if request.POST.get('bill_street') != '':
                    for element in billing_address_obj.values('street'):
                        if request.POST.get('bill_street') != element.get('street'):
                            billing_address_obj.update(street=request.POST.get('bill_street'))

                if request.POST.get('bill_house_number') != '':
                    for element in billing_address_obj.values('house_number'):
                        if request.POST.get('bill_house_number') != element.get('house_number'):
                            billing_address_obj.update(house_number=request.POST.get('bill_house_number'))

                if request.POST.get('bill_address_info') != '':
                    for element in billing_address_obj.values('address_info'):
                        if request.POST.get('bill_address_info') != element.get('address_info'):
                            billing_address_obj.update(address_info=request.POST.get('bill_address_info'))

                if request.POST.get('bill_postal_code') != '':
                    for element in billing_address_obj.values('postal_code'):
                        if request.POST.get('bill_postal_code') != element.get('postal_code'):
                            billing_address_obj.update(postal_code=request.POST.get('bill_postal_code'))

                if request.POST.get('bill_city') != '':
                    for element in billing_address_obj.values('city'):
                        if request.POST.get('bill_city') != element.get('city'):
                            billing_address_obj.update(city=request.POST.get('bill_city'))

                if request.POST.get('bill_country') != '':
                    for element in billing_address_obj.values('country'):
                        if request.POST.get('bill_country') != element.get('country'):
                            billing_address_obj.update(country=request.POST.get('bill_country'))

        neworder = Order()
        neworder.user = request.user
        neworder.fname = request.POST.get('fname')
        neworder.lname = request.POST.get('lname')
        neworder.email = request.POST.get('email')
        neworder.phone = request.POST.get('phone')
        neworder.street = request.POST.get('street')
        neworder.house_number = request.POST.get('house_number')
        neworder.address_info = request.POST.get('address_info')
        neworder.postal_code = request.POST.get('postal_code')
        neworder.city = request.POST.get('city')
        neworder.country = request.POST.get('country')

        if request.POST.get('check_box') != 'true':
            neworder.bill_address_dif = True
            neworder.bill_fname = request.POST.get('bill_fname')
            neworder.bill_lname = request.POST.get('bill_lname')
            neworder.bill_email = request.POST.get('bill_email')
            neworder.bill_phone = request.POST.get('bill_phone')
            neworder.bill_street = request.POST.get('bill_street')
            neworder.bill_house_number = request.POST.get('bill_house_number')
            neworder.bill_address_info = request.POST.get('bill_address_info')
            neworder.bill_postal_code = request.POST.get('bill_postal_code')
            neworder.bill_city = request.POST.get('bill_city')
            neworder.bill_country = request.POST.get('bill_country')

        # neworder.total_price = request.POST.get('total_price_calc')

        neworder.payment_mode = request.POST.get('payment_mode')
        neworder.payment_id = request.POST.get('payment_id')

        cart = Cart.objects.filter(user=request.user, )
        cart_total_price = 0
        for item in cart:
            cart_total_price = cart_total_price + item.product.selling_price * item.product_quantity

        neworder.total_price = "{:.2f}".format(cart_total_price)

        trackingno = 'miaggio#order#' + str(random.randint(1111111, 9999999))
        while Order.objects.filter(tracking_no=trackingno) is None:
            trackingno = 'miaggio#order#' + str(random.randint(1111111, 9999999))

        neworder.tracking_no = trackingno
        neworder.save()

        neworderitmes = Cart.objects.filter(user=request.user)
        for item in neworderitmes:
            OrderItem.objects.create(
                order=neworder,
                product=item.product,
                price=item.product.selling_price,
                quantity=item.product_quantity
            )

            # Ordered quantity must be removed from available stock
            orderproduct = Product.objects.filter(id=item.product_id).first()
            orderproduct.quantity = orderproduct.quantity - item.product_quantity
            orderproduct.save()

        # Users cart must be cleared
        Cart.objects.filter(user=request.user).delete()

        payMode = request.POST.get('payment_mode')
        if payMode == "Paid with PayPal":
            return JsonResponse({'status': "Vielen Dank für Ihren Kauf!"})
        else:
            sweetify.toast(request, "Vielen Dank für Ihren Kauf!", width='275px')

    return redirect('/')