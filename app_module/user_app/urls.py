from django.urls import path,include
from app_module.user_app import views

urlpatterns = [
    path('',views.index_view,name='index_view'),
    path('about_view/',views.about_view,name='about_view'),
    path('cart_view/',views.cart_view,name='cart_view'),
    path('checkout_view/',views.checkout_view,name='checkout_view'),
    path('razorpay_callback/',views.razorpay_callback,name='razorpay_callback'),
    path('invoice_view/<int:order_id>/',views.invoice_view,name='invoice_view'),
    path('contact_view/',views.contact_view,name='contact_view'),
    path('fzf_view/',views.fzf_view,name='fzf_view'),
    path('news_view/',views.news_view,name='news_view'),
    path('shop_view/',views.shop_view,name='shop_view'),
    path('single_news_view/',views.single_news_view,name='single_news_view'),
    path('single_product_view/<int:id>/', views.single_product_view, name='single_product_view'),

    path('subscribe_view/',views.subscribe_view,name='subscribe_view'),

    path('pages_register/',views.pages_register,name='pages_register'),
    path('pages_login/',views.pages_login,name='pages_login'),
    path('logout_view/',views.logout_view,name='logout_view'),

    path('auth_base_view', views.auth_base_view, name='auth_base_view'),

    path('cart/cart_add/<int:id>/', views.cart_add, name='cart_add'),
    path('cart/item_clear/<int:id>/', views.item_clear, name='item_clear'),
    path('cart/item_increment/<int:id>/',views.item_increment, name='item_increment'),
    path('cart/item_decrement/<int:id>/',views.item_decrement, name='item_decrement'),
    path('cart/cart_clear/', views.cart_clear, name='cart_clear'),
    # path('cart/cart-detail/',views.cart_detail,name='cart_detail'),


]
