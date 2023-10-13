from django.urls import path

from . import views

app_name = "auctions"

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create_listing, name="create"),
    path("listing/<int:listing_id>", views.visit_listing, name="listing"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("manage", views.manage, name="manage"),
    path("profile/<int:user_id>", views.account, name="profile"),
    path("edit/<int:listing_id>", views.edit, name="edit"),
    path("categories", views.categories, name="categories"),
    path("category/<int:category_id>", views.category, name="category")
]