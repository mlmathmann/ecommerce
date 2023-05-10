from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from store.models import Cart, Order, OrderItem, Product

import random

@login_required(login_url='loginpage')
def index(request):
    rawcart = Cart.objects.filter(user=request.user)
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

    context = {'cartitems': cartitems,
               'total_price': new_total_price}
    return render(request, 'store/checkout.html', context)


@login_required(login_url='loginpage')
def placeorder(request):
    if request.method == 'POST':
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

        # neworder.total_price = request.POST.get('total_price')

        neworder.payment_mode = request.POST.get('payment_mode')

        cart = Cart.objects.filter(user=request.user, )
        cart_total_price = 0
        for item in cart:
            cart_total_price = cart_total_price + item.product.selling_price * item.product_quantity

        neworder.total_price = cart_total_price

        trackingno = 'miaggio#delivery#' + str(random.randint(1111111, 9999999))
        while Order.objects.filter(tracking_no=trackingno) is None:
            trackingno = 'miaggio#delivery#' + str(random.randint(1111111, 9999999))

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
        messages.success(request, "Your order has been placed successfully")

    return redirect('/')