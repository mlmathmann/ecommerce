from django.urls import path
from . import views
from store.controller import authview, cart, wishlist, checkout, dashboard, midjourney, orders, newsletter, essentials
from django.contrib.auth import views as auth_views
from .views import PasswordsChangeView
from django.conf import settings
from django.conf.urls.static import static
import midjourneyapi.search as search

# the routing and different paths for the pages are listed here and combined with their associated functions,
# e. g. the first path is the homepage, is called using the name "home" as href in the html document and
# is displayed using the render that is returned in the views.home function that gets called when the given
# html element with the href is selected
urlpatterns = [
                  path('', views.home, name="home"),
                  path('categories/<str:slug>', views.categoriesview, name="categoriesview"),
                  path('categories/<str:cate_slug>/<str:prod_slug>', views.productview, name="productview"),

                  path('collections/<str:style>', views.stylecollections, name="stylecollections"),
                  path('collections/<str:style>/products', views.stylecollectionsproducts,
                       name="stylecollectionsproducts"),
                  path('collections/<str:style_slug>/<str:prod_slug>', views.styleproductview,
                       name="styleproductview"),

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

                  path('subscribe-to-newsletter', newsletter.subscribe, name="subscribenewsletter"),
                  path('unsubscribe-from-newsletter', newsletter.unsubscribe, name="unsubscribenewsletter"),

                  path('add-to-cart', cart.addtocart, name="addtocart"),
                  path('cart', cart.viewcart, name="cart"),
                  path('update-cart', cart.updatecart, name='updatecart'),
                  path('delete-cart-item', cart.deletecartitem, name="deletecartitem"),

                  path('generate-creation', midjourney.generatecustomfurniture, name="generatecustomfurniture"),
                  path('cancel-creation', midjourney.cancelcustomfurniture, name="cancelcustomfurniture"),
                  path('create', search.creation, name="creation"),
                  path('request-creation', midjourney.requestfurniture, name="requestfurniture"),

                  path('wishlist', wishlist.index, name="wishlist"),
                  path('add-to-wishlist', wishlist.addtowishlist, name="addtowishlist"),
                  path('delete-wishlist-item', wishlist.deletewishlistitem, name="deletewishlistitem"),

                  path('checkout', checkout.index, name="checkout"),
                  path('place-order', checkout.placeorder, name="placeorder"),

                  path('my-orders', orders.orders_index, name="myorders"),
                  path('my-orders/<str:order>', orders.orders_view, name="myordersdetails"),
                  path('my-creations', orders.furniture_index, name="myfurniture"),
                  path('my-creations/<str:creation_tracking_no>', orders.furniture_view, name="myfurnituredetails"),

                  path('about-us', essentials.about_us, name="about-us"),
                  path('agb', essentials.agb, name="agb"),
                  path('datenschutzrichtlinie', essentials.datenschutz, name="datenschutz"),
                  path('faq', essentials.faq, name="faq"),
                  path('impressum', essentials.impressum, name="impressum"),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
