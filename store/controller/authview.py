from django.shortcuts import redirect, render
from django.contrib import messages
from store.forms import CustomUserForm


def register(request):
    form = CustomUserForm()
    if request.method == "POST":
        form = CustomUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration succsessfull! Please log in to continue!")
            return redirect('/login')
    context = {'form': form}
    return render(request, "store/auth/register.html", context)


def loginpage(request):
    return render(request, "store/auth/login.html")

