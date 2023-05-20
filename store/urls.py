from django.urls import path
from . import views
from store.controller import authview, cart, wishlist, checkout, dashboard
from django.contrib.auth import views as auth_views
from .views import PasswordsChangeView

urlpatterns = [
    path('', views.home, name="home"),
    path('collections', views.collections, name="collections"),
    path('collections/<str:slug>', views.collectionsview, name="collectionsview"),
    path('collections/<str:cate_slug>/<str:prod_slug>', views.productview, name="productview"),

    path('register/', authview.register, name="register"),
    path('login/', authview.loginpage, name="loginpage"),
    path('logout/', authview.logoutpage, name="logout"),
    path('update-user/', authview.updateuser, name="updateuser"),
    #path('update-password/', PasswordsChangeView.as_view(template_name="store/updatepassword.html"), name="updatepassword"),
    path('update-password/', authview.updatepassword, name="updatepassword"),
    path('update-profile/', authview.updateprofile, name="updateprofile"),

    path('myprofile/<str:user>', dashboard.profile, name="profile"),
    path('myprofile/<str:user>/details', dashboard.details, name="details"),

    path('add-to-cart', cart.addtocart, name="addtocart"),
    path('cart', cart.viewcart, name="cart"),
    path('update-cart', cart.updatecart, name='updatecart'),
    path('delete-cart-item', cart.deletecartitem, name="deletecartitem"),

    path('wishlist', wishlist.index, name="wishlist"),
    path('add-to-wishlist', wishlist.addtowishlist, name="addtowishlist"),
    path('delete-wishlist-item', wishlist.deletewishlistitem, name="deletewishlistitem"),

    path('checkout', checkout.index, name="checkout"),
    path('place-order', checkout.placeorder, name="placeorder"),
]
