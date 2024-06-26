from django.urls import path
from accounts.views import *
urlpatterns = [
    path('login/',login_page, name="login"),
    path('register/',register_page, name="register"),
    path('add-to-cart/<uid>/',add_to_cart,name="add_to_cart"),
    path('cart/',cart,name="cart"),
    path('remove-cart/<cart_item_uid>/',remove_cart,name="remove_cart"),
    path('remove-coupon/<cart_id>/',remove_coupon,name="remove_coupon"),
    path('success/',success,name="success"),
    path('pdfs/invoice/', invoice, name='invoice'),
    
]