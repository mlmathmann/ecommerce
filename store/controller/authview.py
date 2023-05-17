from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from store.forms import CustomUserForm, User
from django.contrib.auth.decorators import login_required
from store.models import Profile
from .dashboard import details


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
    user = request.user

    profile_obj = Profile.objects.filter(id=request.user.id).first()
    user_obj = User.objects.filter(id=request.user.id).first()

    profile_obj.phone = request.POST.get('phone')
    profile_obj.street = request.POST.get('street')
    profile_obj.house_number = request.POST.get('house_number')
    profile_obj.address_info = request.POST.get('address_info')
    profile_obj.postal_code = request.POST.get('postal_code')
    print(request.POST.get('postal_code'))
    profile_obj.city = request.POST.get('city')
    profile_obj.save()
    #profile_obj.country = request.POST.get('country')

    user_obj.email = request.POST.get('email')
    user_obj.first_name = request.POST.get('fname')
    user_obj.last_name = request.POST.get('lname')
    user_obj.save()
    messages.success(request, "Profile updated successfully!")
    return details(request, user)
    #return render(request, "store/profile.html")



'''
def updateaccount(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        form = CustomUserForm(request.POST or None, instance=current_user)
        return render(request, "store/updateprofile.html", {'form': form})
    else:
        messages.error(request, "You must login to edit your profile")
        return redirect('/login')
'''