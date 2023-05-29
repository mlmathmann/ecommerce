from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, views
from store.forms import CustomUserForm, User, CustomUserChangeForm, CustomPasswordChangeForm, ProfilePictureChangeForm
from django.contrib.auth.decorators import login_required
from store.models import GeneratedItem
from .dashboard import details, profile
from store.views import get_navbar_context


gen_comp = ''

@login_required(login_url='loginpage')
def generatecustomfurniture(request):
    nav_context = get_navbar_context(request)
    gen_item = None
    global gen_comp
    print("global", gen_comp)

    if request.method == 'POST' and request.POST.get('end') == 'ye':
        gen_comp = ''
    else:
        if request.method == 'POST':
            gen_comp = request.POST.get('gen_comp')
            print("post", gen_comp)

        if gen_comp == 'true':
            gen_items = GeneratedItem.objects.filter(user=request.user).order_by('-created_at')
            gen_item = gen_items.first()

    print(gen_item)
    return render(request, "store/midjourney.html", {'category': nav_context.get('categories'),
                                                     'nav_context': nav_context,
                                                     'profile_picture': nav_context.get('profile_picture'),
                                                     'collections': nav_context.get('collections'),
                                                     'gen_item': gen_item})
