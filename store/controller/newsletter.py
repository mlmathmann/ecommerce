from django.shortcuts import redirect
from store.models import Product, Profile, User
from store.views import get_navbar_context
import sweetify


def subscribe(request):
    if request.method == 'POST':
        email_address = request.POST.get('EMAIL')

        profile_user = Profile.objects.filter(user=request.user).first()
        currentuser = User.objects.filter(id=request.user.id).first()

        if email_address == currentuser.email:
            profile_user.newsletter_subscription = True
            profile_user.save()
        else:
            sweetify.warning(request, 'The entered email does not belong to your acount.')
            return redirect("/")
        sweetify.success(request, 'Subscribed sucessfully!')
    return redirect("/")


def unsubscribe(request):
    profile_user = Profile.objects.filter(user=request.user).first()

    profile_user.newsletter_subscription = False
    profile_user.save()

    sweetify.success(request, 'Unsubscribed sucessfully!')
    return redirect("/")