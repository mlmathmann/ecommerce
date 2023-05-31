from django.shortcuts import redirect, render
from store.views import get_navbar_context


def about_us(request):
    nav_context = get_navbar_context(request)
    context = {'category': nav_context.get('categories'),
               'profile_picture': nav_context.get('profile_picture'), 'collections': nav_context.get('collections'),
               'user_newsletter_subscription': nav_context.get('user_newsletter_subscription')}
    return render(request, "store/essentials/about-us.html", context)


def agb(request):
    nav_context = get_navbar_context(request)
    context = {'category': nav_context.get('categories'),
               'profile_picture': nav_context.get('profile_picture'), 'collections': nav_context.get('collections'),
               'user_newsletter_subscription': nav_context.get('user_newsletter_subscription')}
    return render(request, "store/essentials/agb.html", context)


def datenschutz(request):
    nav_context = get_navbar_context(request)
    context = {'category': nav_context.get('categories'),
               'profile_picture': nav_context.get('profile_picture'), 'collections': nav_context.get('collections'),
               'user_newsletter_subscription': nav_context.get('user_newsletter_subscription')}
    return render(request, "store/essentials/datenschutz.html", context)


def faq(request):
    nav_context = get_navbar_context(request)
    context = {'category': nav_context.get('categories'),
               'profile_picture': nav_context.get('profile_picture'), 'collections': nav_context.get('collections'),
               'user_newsletter_subscription': nav_context.get('user_newsletter_subscription')}
    return render(request, "store/essentials/faq.html", context)


def impressum(request):
    nav_context = get_navbar_context(request)
    context = {'category': nav_context.get('categories'),
               'profile_picture': nav_context.get('profile_picture'), 'collections': nav_context.get('collections'),
               'user_newsletter_subscription': nav_context.get('user_newsletter_subscription')}
    return render(request, "store/essentials/impressum.html", context)
