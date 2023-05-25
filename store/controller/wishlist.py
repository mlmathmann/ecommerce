from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from store.models import Product, Cart, Wishlist
from store.views import get_navbar_context


@login_required(login_url='loginpage')
def index(request):
    nav_context = get_navbar_context(request)
    wishlist = Wishlist.objects.filter(user=request.user)
    context = {'wishlist': wishlist, 'categories': nav_context.get('categories'), 'profile_picture': nav_context.get('profile_picture'), 'collections': nav_context.get('collections')}
    return render(request, 'store/wishlist.html', context)


def addtowishlist(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            prod_id = int(request.POST.get('product_id'))
            product_check = Product.objects.get(id=prod_id)
            if product_check:
                if Wishlist.objects.filter(user=request.user, product_id=prod_id):
                    return JsonResponse({'status': "Product already on wishlist"})
                else:
                    Wishlist.objects.create(user=request.user, product_id=prod_id)
                    return JsonResponse({'status': "Added to wishlist successfully"})
            else:
                return JsonResponse({'status': "This product can't be found"})
        else:
            return JsonResponse({'status': "Login to continue"})
    return redirect('/')


def deletewishlistitem(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            prod_id = int(request.POST.get('product_id'))

            if Wishlist.objects.filter(user=request.user, product_id=prod_id):
                wishlistitem = Wishlist.objects.get(product_id=prod_id)
                wishlistitem.delete()
                index(request)
                return JsonResponse({'status': "Removed from wishlist successfully"})
            else:
                Wishlist.objects.create(user=request.user, product_id=prod_id)
                return JsonResponse({'status': "Product not found in wishlist"})
        else:
            return JsonResponse({'status': "Login to continue"})

    return redirect('/')
