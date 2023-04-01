from time import time
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from datetime import datetime

from .models import User, AuctionListings, Comments, Bids
from .forms import CreateListing, Comment, Category, Bid


def index(request):
    return render(request, "auctions/index.html", ({
        "auctions": AuctionListings.objects.all()
    }))


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def listing(request, listing_id):
    listing = AuctionListings.objects.get(id=listing_id)
    comments = Comments.objects.filter(item_id=listing_id)
    #is the user in watchlist
    userInWatchlist = request.user in listing.watchlist.all()
    bids = Bids.objects.filter(item_id=listing).last()
    allBids = Bids.objects.filter(item_id=listing)
    return render(request, "auctions/listing.html", {
        "listing": listing,
        "comments": comments,
        "formComment": Comment(),
        "formBid": Bid(),
        "UserInWatchlist": userInWatchlist,
        "bids": bids,
        "allBids": allBids
    })

def category(request):
    if request.method == "POST":
        form = Category(request.POST)
        if form.is_valid():
            category = form.cleaned_data['category']
            filter = AuctionListings.objects.filter(category=category)
            return render(request, "auctions/category.html",{
                "form": Category(),
                "auctions": filter
    })
    return render(request, "auctions/category.html",{
        "form": Category(),
        "auctions": AuctionListings.objects.all()
    })

@login_required
def createListing(request):
    if request.method == "POST":
        form = CreateListing(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            textDescription = form.cleaned_data['textDescription']
            startingBid = form.cleaned_data['startingBid']
            imageURL = form.cleaned_data['imageURL']
            category = form.cleaned_data['category']
            creator_id = request.user
            listing = AuctionListings.objects.create(title=title, description=textDescription, starting_price=startingBid, URL_image=imageURL, category=category, creator_id=creator_id)
            
            #return HttpResponseRedirect(reverse("index"))
            return render(request, "auctions/index.html", {
                "message": "Listing Created!",
                "auctions": AuctionListings.objects.all()
            })
    return render(request, "auctions/createListing.html", {
        "form": CreateListing()
    })

@login_required
def watchlist(request):
    # The reversed function will put the last watchlist in the begining of the list
    watchlist = reversed(request.user.users_watchlist.all())
    return render(request, "auctions/watchlist.html", {
        "watchlist": watchlist
    })

@login_required
def addComment(request, listing_id):
    if request.method == "POST":
        form = Comment(request.POST)
        if form.is_valid():
            comment = form.cleaned_data['comment']
            creator_id = request.user
            comments = Comments.objects.create(user_id=creator_id, item_id=AuctionListings.objects.get(id=listing_id), comments=comment)
            comments.save()
            return HttpResponseRedirect(reverse("listing", args=(listing_id, )))

@login_required
def removeWatchlist(request, listing_id):
    listing = AuctionListings.objects.get(id=listing_id)
    user = request.user
    listing.watchlist.remove(user)
    return HttpResponseRedirect(reverse("listing", args=(listing_id, )))


@login_required
def addWatchlist(request, listing_id):
    listing = AuctionListings.objects.get(id=listing_id)
    user = request.user
    listing.watchlist.add(user)
    return HttpResponseRedirect(reverse("listing", args=(listing_id, )))

@login_required
def placeBid(request, listing_id):
    listing = AuctionListings.objects.get(id=listing_id)
    if request.method == "POST":
        if listing.current_state != False:
            form = Bid(request.POST)
            if form.is_valid():
                bid = float(form.cleaned_data['bid'])
                #Check if the bid is bigger than the start price and check if exist current price or the bid is bigger than the current price
                if bid>listing.starting_price and (listing.current_price is None or bid>listing.current_price):
                    listing.current_price = bid
                    user = request.user
                    addBid = Bids.objects.create(user_id=user, item_id=listing, bid=bid)
                    addBid.save()
                    listing.save()
                    return HttpResponseRedirect(reverse("listing", args=(listing_id, )))
                else:
                    listing = AuctionListings.objects.get(id=listing_id)
                    comments = Comments.objects.filter(item_id=listing_id)
                    #is the user in watchlist
                    userInWatchlist = request.user in listing.watchlist.all()
                    return render(request, "auctions/listing.html", {
                        "listing": listing,
                        "comments": comments,
                        "formComment": Comment(),
                        "formBid": Bid(),
                        "UserInWatchlist": userInWatchlist,
                        "message": "Bid to small!"
                    })


@login_required
def closeListing(request, listing_id):
    listing = AuctionListings.objects.get(id=listing_id)
    if request.user == listing.creator_id:
        listing.current_state = False
        listing.save()
        bid = Bids.objects.filter(item_id=listing).last()
        bid.winner = True
        bid.save()
        return HttpResponseRedirect(reverse("listing", args=(listing_id, )))

@login_required
def myItem(request):
    user = request.user
    bids = Bids.objects.filter(user_id=user, winner=True)
    allAuctions = AuctionListings.objects.filter(creator_id=user)
    return render(request, "auctions/myItem.html", {
        "auctions": bids,
        "allAuctions": allAuctions
    })