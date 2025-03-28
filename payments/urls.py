from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('checkout/', views.checkout, name='checkout'),
    path('payment/success/<int:order_id>/', views.payment_success, name='payment_success'),
    path('payment/cancel/', views.payment_cancel, name='payment_cancel'),
] 