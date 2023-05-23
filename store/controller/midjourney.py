from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, views
from store.forms import CustomUserForm, User, CustomUserChangeForm, CustomPasswordChangeForm, ProfilePictureChangeForm
from django.contrib.auth.decorators import login_required
from store.models import Profile
from .dashboard import details, profile
from store.views import get_navbar_context


def generatecustomfurniture(request):
    return render(request, "store/midjourney.html")