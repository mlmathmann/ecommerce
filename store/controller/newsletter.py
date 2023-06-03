from django.shortcuts import redirect
from store.models import Product, Profile, User
import sweetify


# subscribes the user to the newsletter
def subscribe(request):
    if request.method == 'POST':
        if str(request.user) == 'AnonymousUser':
            sweetify.toast(request, 'An account is needed for subscription.', "info", width='275px')
            return redirect("/")
        email_address = request.POST.get('EMAIL')

        profile_user = Profile.objects.filter(user=request.user).first()
        currentuser = User.objects.filter(id=request.user.id).first()

        if email_address == currentuser.email:
            profile_user.newsletter_subscription = True
            profile_user.save()
        else:
            sweetify.toast(request, 'The entered email does not belong to your acount.', "error", width='275px')
            return redirect("/")
        sweetify.toast(request, 'Subscribed sucessfully!', "success", width='275px')
    return redirect("/")


# unsubscribes the user from the newsletter
def unsubscribe(request):
    profile_user = Profile.objects.filter(user=request.user).first()

    profile_user.newsletter_subscription = False
    profile_user.save()

    sweetify.toast(request, 'Unsubscribed sucessfully!', "success", width='275px')
    return redirect("/")