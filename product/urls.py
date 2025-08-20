
from django.urls import path
from .views import signup_view, login_view, logout_view
from . import views

urlpatterns = [
    path("signup/", signup_view, name="signup"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),


    path("dashboard/", views.dashboard, name="dashboard"),
    path("update-location/", views.update_location, name="update_location"),



    path("", views.landing_page, name="landing"),
    path("item/<int:item_id>/", views.item_detail, name="item_detail"),




    path("profile/", views.profile_view, name="profile"),
    path("my-items/", views.my_items_view, name="my_items"),
    path("borrowed-items/", views.borrowed_items_view, name="borrowed_items"),
    path("add-item/", views.add_item, name="add_item"),


]
