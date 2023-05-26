from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, views
from store.forms import CustomUserForm, User, CustomUserChangeForm, CustomPasswordChangeForm, ProfilePictureChangeForm
from django.contrib.auth.decorators import login_required
from store.models import GeneratedItem
from .dashboard import details, profile
from store.views import get_navbar_context


def generatecustomfurniture(request):
    nav_context = get_navbar_context(request)
    gen_items = GeneratedItem.objects.all()
    print(gen_items)
    return render(request, "store/midjourney.html", {'category': nav_context.get('categories'),
                                                     'nav_context': nav_context,
                                                     'profile_picture': nav_context.get('profile_picture'),
                                                     'collections': nav_context.get('collections'),
                                                     'gen_items': gen_items})
