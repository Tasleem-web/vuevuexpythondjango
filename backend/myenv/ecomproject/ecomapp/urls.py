from ecomapp import views
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', views.getRoutes, name="getRoutes"),
    path('products/', views.getProducts, name="getProducts"),
    path('products/<int:product_id>/', views.get_product_by_id, name="getProduct"),
    path('cart/add/', views.postCart, name="postCart"),
    path('cart/', views.getCartItems, name="getCartItems"),
    path('cart/<int:cart_item_id>/', views.removeCartItem, name="removeCartItem"),
    path('members/', views.postMembers, name="postMembers"),
    path('getMembers/', views.getMembers, name="getMembers"),
    path('getMember/<int:member_id>', views.getMember, name="getMember"),
    path('deleteMember/<int:member_id>', views.deleteMember, name="deleteMember"),
    path('updateMember/<int:member_id>', views.updateMember, name="updateMember"),
    path('partialUpdateMember/<int:member_id>', views.partialUpdateMember, name="partialUpdateMember"),
    path('members_with_status/', views.getMembersWithStatus, name="getMembersWithStatus"),
]
