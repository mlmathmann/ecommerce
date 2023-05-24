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

    context = {'category': nav_context.get('categories'), 'products': products,
               'profile_picture': nav_context.get('profile_picture')}
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
        if request.method == 'POST' and request.POST.get('end') == 'ye':
            style_way = ''

        else:
            if request.method == 'POST':
                style_way = request.POST.get('filter_value')

            if style_way != '':
                products = products.filter(style_way=style_way)

        context = {'products': products, 'category': category, 'categories': nav_context.get('categories'),
                   'profile_picture': nav_context.get('profile_picture'), 'style_way': style_way}
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
            context = {'products': products, 'categories': nav_context.get('categories'),
                       'profile_picture': nav_context.get('profile_picture'), 'product_style': product_style}
        else:
            messages.error(request, "No such product found")
            return redirect('collections')
    else:
        messages.error(request, "No such category found")
    return render(request, "store/products/view.html", context)


class PasswordsChangeView(PasswordChangeView):
    form_class = CustomPasswordChangeForm
    success_url = reverse_lazy('home')


def stylecollections(request, style):
    nav_context = get_navbar_context(request)
    style_name = ''
    collection = ''
    collections = ''
    for choice in Product.StyleChoices.choices:
        if choice[1].lower() == style:
            style = choice[0]
            style_name = choice[1]
            collection = Collection.objects.filter(name=style_name.upper()).first()
            collections = Collection.objects.filter().exclude(name=style_name.upper())

    products = Product.objects.filter(style_way=style)
    context = {'collections': collections, 'collection': collection, 'products': products,
               'style_name': style_name.lower(),
               'category': nav_context.get('categories'), 'profile_picture': nav_context.get('profile_picture')}
    return render(request, "store/collections/view.html", context)


category = ''


def stylecollectionsproducts(request, style):
    nav_context = get_navbar_context(request)
    products = Product.objects.filter()
    category_obj = ''

    global category

    if request.method == 'POST' and request.POST.get('end') == 'yeet':
        category = ''

    else:
        if request.method == 'POST':
            category = request.POST.get('filter_value')

        for choice in Product.StyleChoices.choices:
            if choice[1].lower() == style:
                style_choice = choice[0]
                style_name = choice[1]
                style_name.lower()

                products = Product.objects.filter(style_way=style_choice)

                if category != '':
                    products = products.filter(category__slug=category)
                    category_obj = Category.objects.filter(slug=category).first()

    context = {'products': products, 'categories': nav_context.get('categories'),
               'profile_picture': nav_context.get('profile_picture'), 'style_name': style, 'category': category,
               'style_title': Collection.objects.filter(slug=style).first(), 'category_obj': category_obj}
    print(context)
    return render(request, "store/collections/products.html", context)
