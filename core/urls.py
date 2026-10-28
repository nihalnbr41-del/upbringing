from django.urls import path
from . import views
urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("resources/", views.resources, name="resources"),
    path("shop/", views.shop, name="shop"),
    path("register/", views.register, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("portal/", views.dashboard, name="dashboard"),
    path("portal/admin/", views.admin_dashboard, name="admin_dashboard"),
    path("chat/", views.chat, name="chat"),
]
