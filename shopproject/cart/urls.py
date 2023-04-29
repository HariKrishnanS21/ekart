
from django.urls import path

from . import views
app_name='cart'
urlpatterns = [

    path('',views.home,name='home'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/',views.logout,name='logout'),
    path('search/',views.search,name='search'),
    path('cart/',views.cart_details,name='cart_details'),
    path('add/<int:id>/',views.add_cart,name='add_cart'),
    path('remove/<int:id>/',views.item_remove,name='item_remove'),
    path('delete/<int:id>/',views.remove,name='remove'),
    path('<slug:c_slug>/',views.catpage,name='pro_category'),
    path('<slug:c_slug>/<slug:p_slug>/',views.prodetails,name='prodetails'),


]