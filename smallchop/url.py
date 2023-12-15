
from django.urls import path
from . import views
from .views import *
from django.contrib.auth import views as auth_views



urlpatterns = [



    path('home/', views.Index, name='index'),
    path('chops/', views.ChopsView, name='chops'),
    path('chops_detail/<int:product_id>/', views.ChopsDetail,name='chopsdetail'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('checkout_success/', views.checkout_success, name='checkout_success'),
    path('checkout_successfull/', views.checkout_successfull, name='checkout_successfull'),
    path('update_item/', views.updateItem, name='update_item'),
    path('process_order/', views.processOrder, name='process_order'),
    
    
    
    path("dashboard/", views.adminD, name="home"),
    path('admin_user_orders/', admin_user_orders, name='admin_user_orders'),
    path("register/", views.registerPage, name="register"),
    path("orders/", views.userPage, name="user_page"),
    path("profile/", views.ProfilePage, name="profile"),
    path('edit_profile/', edit_profile, name='edit_profile'),
    path("login/", views.loginPage, name="login"),
    path("logout/", views.logoutUser, name="logout"),
   
    path("customer/<str:pk_test>", views.customer, name="customer"),
    path('products/', product_list, name='product_list'),
    path('products/<int:pk>/', product_detail, name='product_detail'),
    path('products/create/', product_create, name='product_create'),
    path('products/<int:pk>/update/', product_update, name='product_update'),
    path('products/<int:pk>/delete/', product_delete, name='product_delete'),
    path('create_category/', create_category, name='create_category'),
    path('create_category/<int:category_id>/', create_category, name='create_category'),
    path("<category>/", views.product_category, name="product_category"),
    
    path('view_comments/', view_comments, name='view_comments'),
    path('approve_comment/<int:comment_id>/', approve_comment, name='approve_comment'),
    path('delete-comment/<int:comment_id>/', delete_comment, name='delete_comment'),

    path('deliveries/', delivery_list, name='delivery-list'),
    path('delivery/add/', delivery_create, name='delivery-add'),
    path('delivery/<int:pk>/', delivery_update, name='delivery-update'),
    path('delivery/<int:pk>/delete/', delivery_delete, name='delivery-delete'),
    
    path('shipping/', shipping_view, name='shipping_view'),
    # Password reset views
    path('password-reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    
    path('password-reset/done', CustomPasswordResetView.as_view(), name='password_reset_done'),

    path('password-reset/confirm/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    
    path('change_password/', change_password_view, name='change_password'),
    

    #Event
    path('evtproducts/', evtproduct_list, name='evtproduct_list'),
    path('evtproducts/<int:pk>/', evtproduct_detail, name='evtproduct_detail'),
    path('evtproducts/create/', evtproduct_create, name='evtproduct_create'),
    path('evtproducts/<int:pk>/update/', evtproduct_update, name='evtproduct_update'),
    path('evtproducts/<int:pk>/delete/', evtproduct_delete, name='evtproduct_delete'),
    path('event_form/', event_form, name='event_form'),
    path('review_page/<int:event_id>/', Review_page, name='review_page'),
    path('checkout/<int:event_id>/', Event_Checkout, name='checkout'),
    path('checkout/success/', checkout_success, name='success_page'),
]