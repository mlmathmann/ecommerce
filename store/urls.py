from django.urls import path
from . import views
from store.controller import authview, cart, wishlist, checkout, dashboard, midjourney
from django.contrib.auth import views as auth_views
from .views import PasswordsChangeView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
                  path('', views.home, name="home"),
                  path('categories/<str:slug>', views.collectionsview, name="collectionsview"),
                  path('categories/<str:cate_slug>/<str:prod_slug>', views.productview, name="productview"),

                  path('collections/<str:style>', views.stylecollections, name="stylecollections"),
                  path('collections/<str:style>/products', views.stylecollectionsproducts, name="stylecollectionsproducts"),

                  path('register/', authview.register, name="register"),
                  path('login/', authview.loginpage, name="loginpage"),
                  path('logout/', authview.logoutpage, name="logout"),
                  path('update-user/', authview.updateuser, name="updateuser"),
                  path('delete-profilepicture/', authview.deleteprofilepicture, name="deleteprofilepicture"),
                  path('update-password/', authview.updatepassword, name="updatepassword"),
                  path('update-profile/', authview.updateprofile, name="updateprofile"),
                  path('delete-user/', authview.deleteuser, name="deleteuser"),

                  path('myprofile/<str:user>', dashboard.profile, name="profile"),
                  path('myprofile/<str:user>/details', dashboard.details, name="details"),

                  path('add-to-cart', cart.addtocart, name="addtocart"),
                  path('cart', cart.viewcart, name="cart"),
                  path('update-cart', cart.updatecart, name='updatecart'),
                  path('delete-cart-item', cart.deletecartitem, name="deletecartitem"),

                  path('generate-custom-furniture', midjourney.generatecustomfurniture, name="generatecustomfurniture"),

                  path('wishlist', wishlist.index, name="wishlist"),
                  path('add-to-wishlist', wishlist.addtowishlist, name="addtowishlist"),
                  path('delete-wishlist-item', wishlist.deletewishlistitem, name="deletewishlistitem"),

                  path('checkout', checkout.index, name="checkout"),
                  path('place-order', checkout.placeorder, name="placeorder"),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
