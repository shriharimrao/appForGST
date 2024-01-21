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
    path("<str:gstin>/create-item", views.create_item, name="create-item"),
    path("<str:gstin>/Upload-item", views.Upload_item, name="Upload-item"),
    path("update-item/<int:pk>", views.update_item, name="update-item"),
    path("delete-item/<int:pk>", views.delete_item, name="delete_item"),
]
