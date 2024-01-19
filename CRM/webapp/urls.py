from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name=""),
    path('register',views.register,name="register"),
    path('my-login',views.my_login,name="my-login"),
    path('user-logout',views.user_logout,name="user-logout"),
    #CRUD
    path('dashboard',views.dashboard,name="dashboard"),
    path('create-invoice',views.create_invoice,name="create-invoice"),
    path('update-invoice/<int:pk>',views.update_invoice,name='update-invoice'),
    path('item/<int:pk>',views.singular_invoice,name="item"),
    path('delete-invoice/<int:pk>',views.delete_invoice,name="delete-invoice"),

]