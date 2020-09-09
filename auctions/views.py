from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from datetime import datetime
from django.forms.models import model_to_dict 
import re

from .models import User, Listing, Bid, Comment, WatchList
from . import utils

def index(request):
    # Skip the first option in the categoryList, since it is blank
    categoryList = Listing.choices[1:]
    listing = Listing.objects.filter(active=True)
    if request.method == "POST":
        if 'listView' in request.POST:
            listView = True
            return render(request,"auctions/index.html", {
                "listing" : listing,
                "categoryList" : categoryList,
                "listView" : listView
            })
    return render(request, "auctions/index.html", {
        "listing" : listing,
        "categoryList" : categoryList
    })

def all_listings(request):
    categoryList = Listing.choices[1:]
    listing = Listing.objects.all()
    
    # Display inactive listings as well
    displayAll = True
    
    if request.method == "POST":
        if 'listView' in request.POST:
            listView = True
            return render(request,"auctions/index.html", {
                "listing" : listing,
                "categoryList" : categoryList,
                "listView" : listView
            })
    return render(request, "auctions/index.html", {
        "listing" : listing,
        "categoryList" : categoryList,
        "displayAll" : displayAll
    })


def login_view(request):
    categoryList = Listing.choices[1:]
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("auction:index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password.",
                "categoryList" : categoryList
            })
    else:
        return render(request, "auctions/login.html", { 
                "categoryList" : categoryList 
                })


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("auction:index"))


def register(request):
    categoryList = Listing.choices[1:]
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match.",
                "categoryList" : categoryList
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken.",
                "categoryList" : categoryList
            })
        login(request, user)
        return HttpResponseRedirect(reverse("auction:index"))
    else:
        return render(request, "auctions/register.html", {
            "categoryList" : categoryList
            })

@login_required
def create(request):
    print(request.user)
    categoryList = Listing.choices[1:]
    if request.method == "POST":
        user = request.user
        title = request.POST['title']
        description = request.POST['description']
        date = datetime.today().strftime('%Y-%m-%d')
        url = request.POST['image-url']
        cat1 = request.POST['cat1']
        cat2 = request.POST['cat2']
        cat3 = request.POST['cat3']
        start_price = request.POST['price']
        condition = request.POST['condition']
        #Create the listing
        listing = Listing.objects.create_listing(user, title, url, cat1, cat2, cat3, condition, description, start_price)
        listing.active = True
        listing.save()
        return render (request, f"auctions/create.html", {
            "listing" : listing,
            "conditionList" : Listing.condition_choices,
            "categoryList" : categoryList
        })
    return render(request, f"auctions/create.html", {
        "choices" : Listing.choices,
        "conditionList" : Listing.condition_choices,
        "categoryList" : categoryList
    })

@login_required
def listing(request, id):
    listing_is_present = False 
    categoryList = Listing.choices[1:]
    listing = Listing.objects.get(id=id)
    recentViewsList = utils.getRecentViewsList(request, listing)
    otherSellersList = utils.getOtherSellers(listing)
    for i in range(len(recentViewsList)) :
        recentViewsList[i] = Listing.objects.get(id=recentViewsList[i])
    print(recentViewsList)
    otherItemsBySeller = utils.getOtherItemsBySeller(listing)
    user = request.user
    # print(user.bids.get(listing=listing))
    winner = None
    comments = utils.getCommentList(listing)
    latestBid = utils.getLatestBid(listing)
    try: 
        watchlist = WatchList.objects.get(user=user, listings=listing)
    except WatchList.DoesNotExist:
        watchlist = None
    if watchlist != None:
        # Listing is present in the Watchlist
        listing_is_present = True 
    if latestBid !=  None:
        latestBidPrice = latestBid.price
    else:
        latestBidPrice = listing.start_price    
    try:
        if user.bids.get(listing=listing).winning_Bid == True:
            winner = user
    except Bid.DoesNotExist:
        pass
    if request.method == "POST":

        # Activate or Deactivate the Listing
        if 'toggle' in request.POST:
            listing.active = not listing.active
            listing.save()
            if listing.active == False:
                try:
                    utils.setBidWinner(listing)
                except Bid.DoesNotExist:
                    pass
                return render(request, f"auctions/listing.html", {
                "listing" : listing,
                "choices" : Listing.choices,
                "categoryList" : categoryList,
                "recentViewsList" : recentViewsList,
                "latestBidPrice" : latestBidPrice,
                "otherItemsList" : otherItemsBySeller,
                "otherSellersList" : otherSellersList,
                "listing_is_present" : listing_is_present
                })
            else:
                try:
                    utils.clearBidWinner(listing)
                except Bid.DoesNotExist:
                    pass
                return render(request, f"auctions/listing.html", {
                "listing" : listing,
                "choices" : Listing.choices,
                "categoryList" : categoryList,
                "latestBidPrice" : latestBidPrice,
                "recentViewsList" : recentViewsList,
                "otherItemsList" : otherItemsBySeller,
                "otherSellersList" : otherSellersList,
                "listing_is_present" : listing_is_present
                })

        #Add functionality for editing/deleting listing later
        elif 'edit' in request.POST or 'delete' in request.POST:
            pass
        
        # Add to Watchlist
        elif 'watchlist' in request.POST:
            utils.makeWatchList(user, listing)
            listing_is_present = True
        
        # Remove from Watchlist
        elif 'remove-watchlist' in request.POST:
            utils.removeFromWatchList(user, listing)
            listing_is_present = False
        
        # Make a Bid
        elif 'bid' in request.POST:
            bidPrice = request.POST['bidPrice']
            utils.makeBid(user, listing, bidPrice)
            latestBid = utils.getLatestBid(listing)
            latestBidPrice = latestBid.price
            

        # Add a comment
        elif 'comment' in request.POST:
            print(request.POST)
            comment = request.POST['comment-text']
            utils.addComment(listing, user, comment)
            comment = utils.getCommentList(listing)
    return render(request, f"auctions/listing.html", { 
        "listing" : listing, 
        "winner" : winner,
        "comments" : comments,
        "categoryList" : categoryList,
        "latestBidPrice" : latestBidPrice,
        "recentViewsList" : recentViewsList,
        "otherItemsList" : otherItemsBySeller,
        "otherSellersList" : otherSellersList,
        "listing_is_present" : listing_is_present
        })


def category(request):
    categoryList = Listing.choices[1:]
    categoryPoster = utils.getCategoryPosters()
    finalCategoryList = []
    for i in range(len(categoryList)):
        finalCategoryList.append((categoryList[i],categoryPoster[i]))
    return render(request, f"auctions/categoryList.html", {
         "categoryList" : categoryList,
         "finalCategoryList" : finalCategoryList
         })


def categoryFiltered(request, cat):
    categoryListForDropDown = Listing.choices[1:]
    listing = Listing.objects.filter(Q(cat1=cat) | Q(cat2=cat) | Q(cat3=cat))
    categoryList = Listing.choices
    for category in categoryList:
        if cat == category[0]:
            humanReadableValue = category[1]
            break
    print(humanReadableValue)
    return render(request, f"auctions/category.html", {
        "category" : humanReadableValue,
        "listing" : listing,
        "categoryList": categoryListForDropDown
    })


def watchlist(request):
    categoryListForDropDown = Listing.choices[1:]
    user = request.user
    if request.user.is_authenticated:
        try:
            watchList = WatchList.objects.get(user=user)
        except WatchList.DoesNotExist:
            watchList = None
        if watchList != None:
            if request.method == "POST":
                keys = request.POST.keys()
                for key in keys:
                    if re.findall("remove-watchlist$",key):
                        arr = key.split('-')
                        ID = arr[0]
                        listing = Listing.objects.get(id=ID)
                        utils.removeFromWatchList(user, listing)
                        break
            return render(request, f"auctions/watchlist.html", {
                "watchListItems" : watchList.listings.all(),
                "categoryList": categoryListForDropDown            
            })
    return render(request, f"auctions/watchlist.html", { "categoryList": categoryListForDropDown })
    