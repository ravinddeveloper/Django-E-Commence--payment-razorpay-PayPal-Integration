from django.urls import path,include
from .views import *
urlpatterns = [
    path('',dashboard,name="dashboard"),
    path('filter',search,name="search"),
    path('add-address/',add_address.as_view(),name="add_address"),
    path('set-default/<id>',set_default,name="set_default"),
    path('restore/<id>',restore,name="restore"),
    path('hide_address/<id>',hide_address,name="hide_address"),
    path('add-to-cart/<id>',add_to_cart,name="add_to_cart"),
    path('minus/<id>',minus,name="minus"),
    path('plus/<id>',plus,name="plus"),
    path('cart/',cart_data,name="cart_data"),
    path('delete-cart-item/<id>',delete_cart_item,name="delete_cart_item"),
    path('clear-cart',clear_cart,name="clear_cart"),
    path('buy/<id>',buy_page,name="buy_page"),
    path('buy_now/<id>',buy_now,name="buy_now"),
    path('place-order/<id>',place_order,name="place_order"),
    path('my-orders',my_orders,name="orders"),
    path('newsletter/',updates,name="updates"),



    # payment

    path('success/',success,name="success"),
    path('success/<product_id>/<order_id>',success_paypal,name="success_p"),
    path('failed/',failed,name="failed"),
    path('failed_paypal/',failed_paypal,name="failed_paypal"),
    path('paypal/', include("paypal.standard.ipn.urls")),

   
]
