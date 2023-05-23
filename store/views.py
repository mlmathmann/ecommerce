from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.forms import PasswordChangeForm
from .models import *
from django.urls import reverse_lazy
from .forms import CustomPasswordChangeForm


# Create your views here.
#
def get_navbar_context(request):
    if Profile.objects.filter(user=request.user.id).values('profile_picture').count() > 0:
        profile_picture = Profile.objects.filter(user=request.user).values('profile_picture')
        for picture in profile_picture:
            profile_picture = picture.get('profile_picture')
    else:
        profile_picture = None
    categories = Category.objects.all()
    context = {'categories': categories, 'profile_picture': profile_picture}
    return context


def home(request):
    nav_context = get_navbar_context(request)
    products = Product.objects.all()

    context = {'category': nav_context.get('categories'), 'products': products, 'profile_picture': nav_context.get('profile_picture')}
    return render(request, "store/index.html", context)


def collections(request):
    category = Category.objects.filter(status=0)
    context = {'category': category}
    return render(request, "store/collections.html", context)


style_way = ''


def collectionsview(request, slug):
    nav_context = get_navbar_context(request)
    if Category.objects.filter(slug=slug, status=0):
        products = Product.objects.filter(category__slug=slug)
        category = Category.objects.filter(slug=slug).first()
        global style_way
        if request.method == 'POST':
            style_way = request.POST.get('option_value')
        if style_way != '':
            if style_way == 'ARISTROCRATIC':
                style_way = Product.StyleChoices.ARISTROCRATIC
            elif style_way == 'IMAGINATIVE':
                style_way = Product.StyleChoices.IMAGINATIVE
            elif style_way == 'FUTURISTIC':
                style_way = Product.StyleChoices.FUTURISTIC
            elif style_way == 'BRUTALISTIC':
                style_way = Product.StyleChoices.BRUTALISTIC
            elif style_way == 'SIMPLICITY':
                style_way = Product.StyleChoices.MINIMALISTIC
            products = products.filter(style_way=style_way)
        context = {'products': products, 'category': category, 'categories': nav_context.get('categories'), 'profile_picture': nav_context.get('profile_picture')}
        return render(request, 'store/products/index.html', context)
    else:
        messages.warning(request, "No such category found")
        return redirect('collections')


def productview(request, cate_slug, prod_slug):
    nav_context = get_navbar_context(request)
    if Category.objects.filter(slug=cate_slug, status=0):
        if Product.objects.filter(slug=prod_slug, status=0):
            products = Product.objects.filter(slug=prod_slug, status=0).first
            product_style = Product.objects.filter(slug=prod_slug, status=0).values('style_way')

            if product_style:
                for style in product_style:
                    product_style = style.get('style_way')
                    for choice in Product.StyleChoices.choices:
                        if product_style == choice[0]:
                            product_style = choice[1]
            else:
                product_style = ''
            context = {'products': products, 'categories': nav_context.get('categories'), 'profile_picture': nav_context.get('profile_picture'), 'product_style': product_style}
        else:
            messages.error(request, "No such product found")
            return redirect('collections')
    else:
        messages.error(request, "No such category found")
    return render(request, "store/products/view.html", context)


class PasswordsChangeView(PasswordChangeView):
    form_class = CustomPasswordChangeForm
    success_url = reverse_lazy('home')