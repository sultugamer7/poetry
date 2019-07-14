from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("register", views.register_view, name="register"),
    path("logout", views.logout_view, name="logout"),
    path("write", views.write_view, name="write"),
    path("profile/<user>", views.profile_view, name="profile"),
    path("read/<int:poem_id>", views.read_view, name="read"),
    path("reset", views.reset_view, name="reset"),
    path("reset/<username>", views.reset_confirm_view, name="reset_confirm"),
    path("edit_profile", views.edit_profile_view, name="edit_profile"),
    path("change_password", views.change_password_view, name="change_password"),
    path("delete_account", views.delete_account_view, name="delete_account"),
    path("rate", views.rate_view, name="rate"),
    path("explore", views.explore_view, name="explore"),
    path("search/<q>", views.search_view, name="search"),
    path("review", views.review_view, name="review"),
    path("notification", views.notification_view, name="notification"),
]
