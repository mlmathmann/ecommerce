import sweetify
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from store.forms import CustomUserForm, User, CustomUserChangeForm, CustomPasswordChangeForm, ProfilePictureChangeForm
from django.contrib.auth.decorators import login_required
from store.models import Profile, BillingAddress
from .dashboard import details, profile
from store.views import get_navbar_context


def register(request):
    nav_context = get_navbar_context(request)
    form = CustomUserForm()
    if request.method == "POST":
        form = CustomUserForm(request.POST)
        if form.is_valid():
            form.save()
            sweetify.toast(request, "Registration succsessful! Please log in to continue!", width='275px')
            return redirect('/login')
    context = {'form': form, 'categories': nav_context.get('categories'),
               'profile_picture': nav_context.get('profile_picture'),
               'collections': nav_context.get('collections'),
               'user_newsletter_subscription': nav_context.get('user_newsletter_subscription')}
    return render(request, "store/auth/register.html", context)


def loginpage(request):
    nav_context = get_navbar_context(request)
    if request.user.is_authenticated:
        sweetify.toast(request, "You are already logged in!", "info", width='275px')
        return redirect("/")
    else:
        if request.method == "POST":
            name = request.POST.get('username')
            user_password = request.POST.get('password')

            user = authenticate(request, username=name, password=user_password)

            if user is not None:
                login(request, user)
                sweetify.toast(request, "Login successful!", width='275px')
                return redirect("/")
            else:
                sweetify.toast(request, "Invalid username or password!", "error", width='275px')
                return redirect('/login')
        context = {'categories': nav_context.get('categories'),
                   'profile_picture': nav_context.get('profile_picture'),
                   'collections': nav_context.get('collections'),
                   'user_newsletter_subscription': nav_context.get('user_newsletter_subscription')}
        return render(request, "store/auth/login.html", context)


def logoutpage(request):
    if request.user.is_authenticated:
        logout(request)
        sweetify.toast(request, "Logout successful!", "success", width='275px')
    return redirect("/")


@login_required(login_url='loginpage')
def updateprofile(request):
    profile_changes = False
    if request.method == 'POST':

        currentuser = User.objects.filter(id=request.user.id).first()

        if request.POST.get('fname') != '':
            if request.POST.get('fname') != currentuser.__getattribute__('first_name'):
                currentuser.first_name = request.POST.get('fname')
                currentuser.save()
                profile_changes = True

        if request.POST.get('lname') != '':
            if request.POST.get('lname') != currentuser.__getattribute__('last_name'):
                currentuser.last_name = request.POST.get('lname')
                currentuser.save()
                profile_changes = True

        profile_obj = Profile.objects.filter(user=request.user)

        if not profile_obj:
            sweetify.toast(request, "Customer data changed successfully!", "success", width='275px')
            return details(request, request.user)

        if request.POST.get('phone') != '':
            for element in profile_obj.values('phone'):
                if request.POST.get('phone') != element.get('phone'):
                    profile_obj.update(phone=request.POST.get('phone'))
                    profile_changes = True

        if request.POST.get('street') != '':
            for element in profile_obj.values('street'):
                if request.POST.get('street') != element.get('street'):
                    profile_obj.update(street=request.POST.get('street'))
                    profile_changes = True

        if request.POST.get('house_number') != '':
            for element in profile_obj.values('house_number'):
                if request.POST.get('house_number') != element.get('house_number'):
                    profile_obj.update(house_number=request.POST.get('house_number'))
                    profile_changes = True

        if request.POST.get('address_info') != '':
            for element in profile_obj.values('address_info'):
                if request.POST.get('address_info') != element.get('address_info'):
                    profile_obj.update(address_info=request.POST.get('address_info'))
                    profile_changes = True

        if request.POST.get('postal_code') != '':
            for element in profile_obj.values('postal_code'):
                if request.POST.get('postal_code') != element.get('postal_code'):
                    profile_obj.update(postal_code=request.POST.get('postal_code'))
                    profile_changes = True

        if request.POST.get('city') != '':
            for element in profile_obj.values('city'):
                if request.POST.get('city') != element.get('city'):
                    profile_obj.update(city=request.POST.get('city'))
                    profile_changes = True

        if request.POST.get('country') != '':
            for element in profile_obj.values('country'):
                if request.POST.get('country') != element.get('country'):
                    profile_obj.update(country=request.POST.get('country'))
                    profile_changes = True

        if BillingAddress.objects.filter(profile__user=request.user):
            billing_address = BillingAddress.objects.filter(profile__user=request.user)
            if request.POST.get('bill_fname') != '':
                for element in billing_address.values('fname'):
                    if request.POST.get('bill_fname') != element.get('fname'):
                        billing_address.update(fname=request.POST.get('bill_fname'))
                        profile_changes = True
                        print("fname")

            if request.POST.get('bill_lname') != '':
                for element in billing_address.values('lname'):
                    if request.POST.get('bill_lname') != element.get('lname'):
                        billing_address.update(lname=request.POST.get('bill_lname'))
                        profile_changes = True

            if request.POST.get('bill_phone') != '':
                for element in billing_address.values('phone'):
                    if request.POST.get('bill_phone') != element.get('phone'):
                        billing_address.update(phone=request.POST.get('bill_phone'))
                        profile_changes = True

            if request.POST.get('bill_street') != '':
                for element in billing_address.values('street'):
                    if request.POST.get('bill_street') != element.get('street'):
                        billing_address.update(street=request.POST.get('bill_street'))
                        profile_changes = True

            if request.POST.get('bill_house_number') != '':
                for element in billing_address.values('house_number'):
                    if request.POST.get('bill_house_number') != element.get('house_number'):
                        billing_address.update(house_number=request.POST.get('bill_house_number'))
                        profile_changes = True

            if request.POST.get('bill_address_info') != '':
                for element in billing_address.values('address_info'):
                    if request.POST.get('bill_address_info') != element.get('address_info'):
                        billing_address.update(address_info=request.POST.get('bill_address_info'))
                        profile_changes = True

            if request.POST.get('bill_postal_code') != '':
                for element in billing_address.values('postal_code'):
                    if request.POST.get('bill_postal_code') != element.get('postal_code'):
                        billing_address.update(postal_code=request.POST.get('bill_postal_code'))
                        profile_changes = True

            if request.POST.get('bill_city') != '':
                for element in billing_address.values('city'):
                    if request.POST.get('bill_city') != element.get('city'):
                        billing_address.update(city=request.POST.get('bill_city'))
                        profile_changes = True

            if request.POST.get('bill_country') != '':
                for element in billing_address.values('country'):
                    if request.POST.get('bill_country') != element.get('country'):
                        billing_address.update(country=request.POST.get('bill_country'))
                        profile_changes = True

        if profile_changes == True:
            sweetify.toast(request, "Profile updated successfully!", "success", width='275px')
            return details(request, request.user)
        sweetify.toast(request, "Profile is already up-to-date!", "info", width='275px')
        return details(request, request.user)


@login_required(login_url='loginpage')
def updateuser(request):
    nav_context = get_navbar_context(request)
    current_user = User.objects.get(id=request.user.id)

    if not Profile.objects.filter(user=request.user):
        profile_user = Profile()
        profile_user.user = request.user
        profile_user.email = ''
        profile_user.phone = ''
        profile_user.street = ''
        profile_user.house_number = ''
        profile_user.address_info = ''
        profile_user.postal_code = ''
        profile_user.city = ''
        profile_user.country = ''
        profile_user.save()

    if not Profile.objects.filter(user=request.user):
        profile_user = Profile()
        profile_user.user = request.user
        profile_user.email = ""
        profile_user.phone = ""
        profile_user.street = ""
        profile_user.house_number = ""
        profile_user.address_info = ""
        profile_user.postal_code = ""
        profile_user.city = ""
        profile_user.country = ""
        profile_user.save()

    profile_user = Profile.objects.filter(user=request.user).first()

    user_form = CustomUserChangeForm(None, instance=current_user)
    profile_form = ProfilePictureChangeForm(None, request.FILES or None, instance=profile_user)
    if request.method == "POST":
        user_form = CustomUserChangeForm(request.POST, request.FILES or None, instance=current_user)
        profile_form = ProfilePictureChangeForm(request.POST, request.FILES or None, instance=profile_user)
        if request.FILES:
            if profile_form.is_valid():
                profile_form.save()
                sweetify.toast(request, "Picture changed successfully!", "success", width='275px')
                return redirect("profile", request.user)
        else:
            if request.POST.get('username') == current_user.get_username() and request.POST.get(
                    'email') == current_user.__getattribute__('email'):
                sweetify.toast(request, "No changes detected!", "info", width='275px')
                return render(request, "store/updateuser.html", {'user_form': user_form, 'profile_form': profile_form,
                                                                 'category': nav_context.get('categories'),
                                                                 'profile_picture': nav_context.get('profile_picture'),
                                                                 'collections': nav_context.get('collections')})
            if user_form.is_valid() and profile_form.is_valid():
                user_form.save()
                profile_form.save()
                sweetify.toast(request, "User Info changed successfully!", "success", width='275px')
                return redirect("profile", request.POST.get('username'))
    return render(request, "store/updateuser.html",
                  {'user_form': user_form, 'profile_form': profile_form, 'categories': nav_context.get('categories'),
                   'profile_picture': nav_context.get('profile_picture'),
                   'collections': nav_context.get('collections')})


@login_required(login_url='loginpage')
def updatepassword(request):
    nav_context = get_navbar_context(request)
    form = CustomPasswordChangeForm(request.user)
    if request.method == "POST":
        form = CustomPasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            sweetify.toast(request, "Password changed successfully!", "success", width='275px')
            return profile(request, request.user)
        else:
            msg = ''
            for error in form.error_messages:
                msg += form.error_messages.get(f'{error}') + "\n\n"
            sweetify.toast(request, f"{msg}", "error", persistent="Close", width='275px')
            return render(request, "store/updatepassword.html",
                          {'form': form, 'categories': nav_context.get('categories'),
                           'profile_picture': nav_context.get('profile_picture'),
                           'collections': nav_context.get('collections')})
    return render(request, "store/updatepassword.html", {'form': form, 'categories': nav_context.get('categories'),
                                                         'profile_picture': nav_context.get('profile_picture'),
                                                         'collections': nav_context.get('collections')})


@login_required(login_url='loginpage')
def deleteprofilepicture(request):
    current_profile = Profile.objects.get(user__id=request.user.id)
    current_profile.profile_picture = None
    current_profile.save()
    sweetify.toast(request, "Picture removed successfully!", "success", width='275px')
    return redirect("profile", request.user)


@login_required(login_url='loginpage')
def deleteuser(request):
    current_user = User.objects.get(id=request.user.id)
    current_user.delete()
    sweetify.toast(request, "Account deleted successfully!", "success", width='275px')
    return redirect("home")
