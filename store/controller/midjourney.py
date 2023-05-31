from django.shortcuts import redirect, render
from store.forms import User
from django.contrib.auth.decorators import login_required
from store.models import GeneratedItem, Creation
from store.views import get_navbar_context
import random
import sweetify


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

        if gen_comp == 'true':
            gen_items = GeneratedItem.objects.filter(user=request.user).order_by('-created_at')
            gen_item = gen_items.first()

    print(gen_item)
    return render(request, "store/midjourney.html", {'category': nav_context.get('categories'),
                                                     'nav_context': nav_context,
                                                     'profile_picture': nav_context.get('profile_picture'),
                                                     'collections': nav_context.get('collections'),
                                                     'gen_item': gen_item})


@login_required(login_url='loginpage')
def requestfurniture(request):
    if request.method == 'POST':
        currentuser = User.objects.filter(id=request.user.id).first()
        gen_items = GeneratedItem.objects.filter(user=request.user).order_by('-created_at')

        creation = Creation()
        creation.user = request.user
        creation.email = currentuser.email
        creation.order = gen_items.first()
        creation.version = request.POST.get('selected')
        creation.message = request.POST.get('message')
        creation.tracking_no = 'miaggio#creation#' + str(random.randint(1111111, 9999999))
        creation.save()
        sweetify.success(request, 'Ihre Anfrage wurde erstellt!')
        return redirect('/')

    return render(request, "store/midjourney.html")


@login_required(login_url='loginpage')
def cancelcustomfurniture(request):
    global gen_comp
    if gen_comp == 'true':
        users_gen_item = GeneratedItem.objects.filter(user=request.user).order_by('-created_at').first()
        users_gen_item.delete()
        print("deleted")
    print("nothing")

    return redirect('generatecustomfurniture')
