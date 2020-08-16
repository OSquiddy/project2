from django.urls import path

from . import views

app_name = "auction"
urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("l/<str:id>", views.listing, name="listing"),
    path("create", views.create, name="create"),
    path("categories", views.category, name="categories"),
    path("c/<str:cat>", views.categoryFiltered, name="filteredByCat"),
    path("all", views.all_listings, name="allListings"),
    path("watchlist", views.watchlist, name="watchlist")
]
