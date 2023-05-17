from django.shortcuts import redirect, render
from django.contrib import messages
from .models import *




# Create your views here.
def home(request):
    categories = Category.objects.all()
    products = Product.objects.all()
    context = {'category': categories, 'products': products}
    return render(request, "store/index.html", context)


def collections(request):
    category = Category.objects.filter(status=0)
    context = {'category': category}
    return render(request, "store/collections.html", context)


style_way = ''


def collectionsview(request, slug):
    if Category.objects.filter(slug=slug, status=0):
        products = Product.objects.filter(category__slug=slug)
        category = Category.objects.filter(slug=slug).first()
        print(request.path, request.body)
        global style_way
        if request.method == 'POST':
            style_way = request.POST.get('option_value')
            print('POST', style_way)
        if style_way != '':
            print(f"POST NO NONE \"{style_way}\"")
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
            print(style_way)
            products = products.filter(style_way=style_way)
        context = {'products': products, 'category': category}
        return render(request, 'store/products/index.html', context)
    else:
        messages.warning(request, "No such category found")
        return redirect('collections')


def productview(request, cate_slug, prod_slug):
    if Category.objects.filter(slug=cate_slug, status=0):
        if Product.objects.filter(slug=prod_slug, status=0):
            products = Product.objects.filter(slug=prod_slug, status=0).first
            context = {'products': products}
        else:
            messages.error(request, "No such product found")
            return redirect('collections')
    else:
        messages.error(request, "No such category found")
    return render(request, "store/products/view.html", context)
