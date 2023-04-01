from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("createListing", views.createListing, name="createListing"),
    path("<int:listing_id>", views.listing, name="listing"),
    path("addComment/<int:listing_id>", views.addComment, name="addComment"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("categoty", views.category, name="category"),
    path("removeWatchlist/<int:listing_id>", views.removeWatchlist, name="removeWatchlist"),
    path("addWatchlist/<int:listing_id>", views.addWatchlist, name="addWatchlist"),
    path("placeBid/<int:listing_id>", views.placeBid, name="placeBid"),
    path("closeListing/<int:listing_id>", views.closeListing, name="closeListing"),
    path("myItem", views.myItem, name="myItem")
]
