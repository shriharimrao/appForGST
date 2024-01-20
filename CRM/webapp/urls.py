from django.urls import path
from . import views


urlpatterns = [
    path("", views.home, name=""),
    path("register", views.register, name="register"),
    path("my-login", views.my_login, name="my-login"),
    path("gst-view", views.gstview, name="gstview"),
    path("create-gstin", views.creategstinform, name="creategstinform"),
    path("user-logout", views.user_logout, name="user-logout"),
    # CRUD
    path("dashboard/<str:gstin>", views.dashboard, name="dashboard"),
    path("<str:gstin>/create-invoice", views.create_invoice, name="create-invoice"),
    path("<str:gstin>/Upload-invoice", views.Upload_invoice, name="Upload-invoice"),
    path("update-invoice/<int:pk>", views.update_invoice, name="update-invoice"),
    path("item/<int:pk>", views.singular_invoice, name="item"),
    path("delete-invoice/<int:pk>", views.delete_invoice, name="delete_invoice"),
]
