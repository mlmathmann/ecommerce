from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, views
from store.forms import CustomUserForm, User, CustomUserChangeForm, CustomPasswordChangeForm, ProfilePictureChangeForm
from django.contrib.auth.decorators import login_required
from store.models import Profile
from .dashboard import details, profile
from store.views import get_navbar_context


def register(request):
    form = CustomUserForm()
    if request.method == "POST":
        form = CustomUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration succsessful! Please log in to continue!")
            return redirect('/login')
    context = {'form': form}
    return render(request, "store/auth/register.html", context)


def loginpage(request):
    if request.user.is_authenticated:
        messages.warning(request, "You are already logged in!")
        return redirect("/")
    else:
        if request.method == "POST":
            name = request.POST.get('username')
            user_password = request.POST.get('password')

            user = authenticate(request, username=name, password=user_password)

            if user is not None:
                login(request, user)
                messages.success(request, "Login successful!")
                return redirect("/")
            else:
                messages.error(request, "Invalid Username or Password!")
                return redirect('/login')
        return render(request, "store/auth/login.html")


def logoutpage(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, "Logout successful!")
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
            messages.success(request, "Customer data changed successfully!")
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

        if profile_changes == True:
            messages.success(request, "Profile updated successfully!")
            return details(request, request.user)
        messages.success(request, "Your profile is already up-to-date!")
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

    profile_user = Profile.objects.filter(user=request.user).first()
    user_form = CustomUserChangeForm(None, instance=current_user)
    profile_form = ProfilePictureChangeForm(None, request.FILES or None, instance=profile_user)
    if request.method == "POST":
        user_form = CustomUserChangeForm(request.POST, request.FILES or None, instance=current_user)
        profile_form = ProfilePictureChangeForm(request.POST, request.FILES or None, instance=profile_user)
        if request.FILES:
            if profile_form.is_valid():
                profile_form.save()
                messages.success(request, "Profilepicture changed successfully!")
                return redirect("profile", request.user)
        else:
            if request.POST.get('username') == current_user.get_username() and request.POST.get(
                    'email') == current_user.__getattribute__('email'):
                messages.success(request, "No changes detected!")
                return render(request, "store/updateuser.html", {'user_form': user_form, 'profile_form': profile_form, 'category': nav_context.get('categories'), 'profile_picture': nav_context.get('profile_picture'),  'collections': nav_context.get('collections')})
            if user_form.is_valid() and profile_form.is_valid():
                user_form.save()
                profile_form.save()
                messages.success(request, "User Info changed successfully!")
                return redirect("profile", request.POST.get('username'))
    return render(request, "store/updateuser.html", {'user_form': user_form, 'profile_form': profile_form, 'category': nav_context.get('categories'), 'profile_picture': nav_context.get('profile_picture'), 'collections': nav_context.get('collections')})


@login_required(login_url='loginpage')
def updatepassword(request):
    nav_context = get_navbar_context(request)
    current_user = User.objects.get(id=request.user.id)
    form = CustomPasswordChangeForm(request.user)
    if request.method == "POST":
        form = CustomPasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Password changed successfully!")
            return profile(request, request.user)
        else:
            for error in form.error_messages:
                msg = form.error_messages.get(f'{error}')
                messages.warning(request, f"{msg}")
            return render(request, "store/updatepassword.html", {'form': form, 'category': nav_context.get('categories'), 'profile_picture': nav_context.get('profile_picture'), 'collections': nav_context.get('collections')})
    return render(request, "store/updatepassword.html", {'form': form, 'category': nav_context.get('categories'), 'profile_picture': nav_context.get('profile_picture'), 'collections': nav_context.get('collections')})


@login_required(login_url='loginpage')
def deleteprofilepicture(request):
    current_profile = Profile.objects.get(user__id=request.user.id)
    current_profile.profile_picture = None
    current_profile.save()
    messages.success(request, "Profilepicture removed successfully!")
    return redirect("profile", request.user)


@login_required(login_url='loginpage')
def deleteuser(request):
    current_user = User.objects.get(id=request.user.id)
    current_user.delete()
    messages.success(request, "Account deleted successfully!")
    return redirect("home")
