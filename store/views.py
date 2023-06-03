import sweetify
from django.shortcuts import redirect, render
from django.contrib.auth.views import PasswordChangeView
from .models import *
from django.urls import reverse_lazy
from .forms import CustomPasswordChangeForm

# Create your views here.

# this function provies the users profile picture, newsletter, categories and collections for the navbar on each page
def get_navbar_context(request):
    user_newsletter_subscription = False

    if Profile.objects.filter(user=request.user.id).values('profile_picture').count() > 0:
        profile_picture = Profile.objects.filter(user=request.user).values('profile_picture')
        for picture in profile_picture:
            profile_picture = picture.get('profile_picture')
    else:
        profile_picture = None
    categories = Category.objects.all()
    collections = Collection.objects.all()

    if request.user.is_authenticated:
        user_newsletter_subscription = Profile.objects.filter(user=request.user).values('newsletter_subscription')
        if user_newsletter_subscription:
            for newsletter_subscription in user_newsletter_subscription:
                user_newsletter_subscription = newsletter_subscription.get('newsletter_subscription')

    context = {'categories': categories, 'profile_picture': profile_picture, 'collections': collections, 'user_newsletter_subscription': user_newsletter_subscription}
    return context


# miaggio's homepage
def home(request):
    nav_context = get_navbar_context(request)
    products = Product.objects.all()
    products = products.order_by('-created_at')[:9]

    context = {'category': nav_context.get('categories'), 'products': products,
               'profile_picture': nav_context.get('profile_picture'), 'collections': nav_context.get('collections'),
               'user_newsletter_subscription': nav_context.get('user_newsletter_subscription')}
    return render(request, "store/index.html", context)


style_way = ''
price_filter = ''


# displays the selected category view e.g. chairs
def categoriesview(request, slug):
    nav_context = get_navbar_context(request)

    if Category.objects.filter(slug=slug, status=0):
        products = Product.objects.filter(category__slug=slug).order_by('name')
        category = Category.objects.filter(slug=slug).first()
        global style_way
        global price_filter
        if request.method == 'POST' and request.POST.get('end') == 'true':
            style_way = ''
            price_filter = ''

        else:
            if request.method == 'POST':
                if request.POST.get('filter_value') is not None:
                    style_way = request.POST.get('filter_value')
                if request.POST.get('price_filter_value') is not None:
                    price_filter = request.POST.get('price_filter_value')

            if style_way != '':
                products = products.filter(style_way=style_way)

            if price_filter != '' and price_filter == 'price desc':
                products = products.order_by('-selling_price')

            elif price_filter != '' and price_filter == 'price asc':
                products = products.order_by('selling_price')

        context = {'products': products, 'category': category, 'categories': nav_context.get('categories'),
                   'profile_picture': nav_context.get('profile_picture'), 'style_way': style_way,
                   'collections': nav_context.get('collections'), 'price_filter': price_filter}
        return render(request, 'store/products/index.html', context)
    else:
        sweetify.toast(request, "No such category found!", "error")
        return redirect('collections')


# displays the selected product of the category, e. g. chair
def productview(request, cate_slug, prod_slug):
    nav_context = get_navbar_context(request)
    if Category.objects.filter(slug=cate_slug, status=0):
        if Product.objects.filter(slug=prod_slug, status=0):
            products = Product.objects.filter(slug=prod_slug, status=0).first

            product_style = Product.objects.filter(slug=prod_slug, status=0).values('style_way')

            if product_style:
                for style in product_style:
                    product_style = style.get('style_way')
                    other_products = Product.objects.filter(style_way=product_style).exclude(slug=prod_slug)[:6]
                    for choice in Product.StyleChoices.choices:
                        if product_style == choice[0]:
                            product_style = choice[1]

            else:
                product_style = ''
                other_products = ''
            context = {'products': products, 'categories': nav_context.get('categories'),
                       'profile_picture': nav_context.get('profile_picture'), 'product_style': product_style,
                       'collections': nav_context.get('collections'), 'other_products': other_products}
        else:
            sweetify.toast(request, "No such product found!", "error")
            return redirect('collections')
    else:
        sweetify.toast(request, "No such category found!", "error")
        context = {'categories': nav_context.get('categories'),
                   'profile_picture': nav_context.get('profile_picture'),
                   'collections': nav_context.get('collections')}
    return render(request, "store/products/view.html", context)


# displays the selected product of the collection, e.g. aristocratic arm chair
def styleproductview(request, style_slug, prod_slug):
    nav_context = get_navbar_context(request)

    all_collections = Collection.objects.all()

    for choice in all_collections:
        if style_slug == choice.style_sign:
            style_slug = choice.style_sign

    if Collection.objects.filter(slug=style_slug):
        if Product.objects.filter(slug=prod_slug, status=0):
            products = Product.objects.filter(slug=prod_slug, status=0).first

            product_style = Product.objects.filter(slug=prod_slug, status=0).values('style_way')

            if product_style:
                for style in product_style:
                    product_style = style.get('style_way')
                    other_products = Product.objects.filter(style_way=product_style).exclude(slug=prod_slug)[:6]
                    for choice in Product.StyleChoices.choices:
                        if product_style == choice[0]:
                            product_style = choice[1]

            else:
                product_style = ''
                other_products = ''
            context = {'products': products, 'categories': nav_context.get('categories'),
                       'profile_picture': nav_context.get('profile_picture'), 'product_style': product_style,
                       'collections': nav_context.get('collections'), 'other_products': other_products}
        else:
            sweetify.toast(request, "No such product found!", "error")
            return redirect('collections')
    else:
        sweetify.toast(request, "No such category found!", "error")
        context = {'categories': nav_context.get('categories'),
                   'profile_picture': nav_context.get('profile_picture'),
                   'collections': nav_context.get('collections')}
    return render(request, "store/products/view.html", context)


# displays the page where a user can change their password
class PasswordsChangeView(PasswordChangeView):
    form_class = CustomPasswordChangeForm
    success_url = reverse_lazy('home')


# displays the selected collection e. g. imaginative on a overview page to introduce you to the theme or style of the
# chosen collection, the other collections can be found listed under the selected one, from there the user can
# view the products of a chosen collection
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
               'categories': nav_context.get('categories'), 'profile_picture': nav_context.get('profile_picture'),
               'collections_nav': nav_context.get('collections')}
    return render(request, "store/collections/view.html", context)


category = ''


# dispalys the products of a collection e. g. imaginative
def stylecollectionsproducts(request, style):
    nav_context = get_navbar_context(request)

    products = Product.objects.filter().order_by('name')

    category_obj = ''
    global category
    global price_filter

    if request.method == 'POST' and request.POST.get('end') == 'true':
        category = ''
        price_filter = ''

    else:
        if request.method == 'POST':
            if request.POST.get('filter_value') is not None:
                category = request.POST.get('filter_value')
            if request.POST.get('price_filter_value') is not None:
                price_filter = request.POST.get('price_filter_value')

        for choice in Product.StyleChoices.choices:
            if choice[1].lower() == style:
                style_choice = choice[0]
                style_name = choice[1]
                style_name.lower()

                products = Product.objects.filter(style_way=style_choice).order_by('name')

                if category != '':
                    products = products.filter(category__slug=category).order_by('name')
                    category_obj = Category.objects.filter(slug=category).first()

                if price_filter != '' and price_filter == 'price desc':
                    products = products.order_by('-selling_price')
                elif price_filter != '' and price_filter == 'price asc':
                    products = products.order_by('selling_price')

    context = {'products': products, 'categories': nav_context.get('categories'),
               'profile_picture': nav_context.get('profile_picture'), 'style_name': style, 'category': category,
               'style_title': Collection.objects.filter(slug=style).first(), 'category_obj': category_obj,
               'collections': nav_context.get('collections'), 'price_filter': price_filter}
    return render(request, "store/collections/products.html", context)
