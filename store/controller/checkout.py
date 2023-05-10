from django.shortcuts import redirect, render
from django.contrib import messages

from django.contrib.auth.decorators import login_required

from store.models import Product, Cart


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
