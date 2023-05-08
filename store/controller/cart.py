from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.contrib import messages

from store.models import Product, Cart


def addtocart(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            prod_id = int(request.POST.get('product_id'))
            product_check = Product.objects.get(id=prod_id)
            if product_check:
                if Cart.objects.filter(user=request.user.id, product_id=prod_id):
                    return JsonResponse({'status': "This product is already in your cart"})
                else:
                    prod_qty = int(request.POST.get('product_qty'))
                    if product_check.quantity >= prod_qty:
                        Cart.objects.create(user=request.user, product_id=prod_id, product_quantity=prod_qty)
                        return JsonResponse({'status': "Product was added successfully"})
                    else:
                        return JsonResponse({'status': "Only " + str(product_check.quantity) + " left in stock"})
            else:
                return JsonResponse({'status': "The product in your cart can't be found"})
        else:
            return JsonResponse({'status': "Login to continue"})
    return redirect('/')


def viewcart(request):
    cart = Cart.objects.filter(user=request.user)
    context = {'cart': cart}
    return render(request, 'store/cart.html', context)
