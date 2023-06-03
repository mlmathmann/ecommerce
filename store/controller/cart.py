from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from store.models import Product, Cart
from store.views import get_navbar_context


# adds a product that is available (in stock) to the users cart
def addtocart(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            prod_id = int(request.POST.get('product_id'))
            product_check = Product.objects.get(id=prod_id)
            if product_check:
                if Cart.objects.filter(user=request.user.id, product_id=prod_id):
                    return JsonResponse({'status': "Product already in cart"})
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


# displays the users cart with all the added products and some basic information to each item
@login_required(login_url='loginpage')
def viewcart(request):
    nav_context = get_navbar_context(request)
    cart = Cart.objects.filter(user=request.user)
    cart_count = cart.count()
    context = {'cart': cart, 'cart_count': cart_count,'categories': nav_context.get('categories'), 'profile_picture': nav_context.get('profile_picture'), 'collections': nav_context.get('collections')}
    return render(request, 'store/cart.html', context)


# displays and saves the cart when the quantity of products are changed
def updatecart(request):
    if request.method == 'POST':
        prod_id = int(request.POST.get('product_id'))
        if Cart.objects.filter(user=request.user, product_id=prod_id):
            prod_qty = int(request.POST.get('product_qty'))
            cart = Cart.objects.get(product_id=prod_id, user=request.user)
            cart.product_quantity = prod_qty
            cart.save()
            return JsonResponse({'status': "Cart updated successfully"})
    return redirect('/')


# removes a product from the cart of a user
def deletecartitem(request):
    if request.method == 'POST':
        prod_id = int(request.POST.get('product_id'))
        if Cart.objects.filter(user=request.user, product_id=prod_id):
            cartitem = Cart.objects.filter(product_id=prod_id, user=request.user)
            cartitem.delete()
        return JsonResponse({'status': "Item removed successfully"})
    return redirect('/')
