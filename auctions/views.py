from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse

from .models import User, Listing, Bids, ListingForm, BidForm, CATEGORIES

def index(request):
    all_listings = Listing.objects.all()

    return render(request, "auctions/index.html", {
        "listings": all_listings
    })

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

@login_required
def create(request):
    #if form has been completed check for validation and save.
    if request.method == "POST":
        form = ListingForm(request.POST)
        if form.is_valid:
            print("Data is Valid")
            listing_data = form.save(commit=False)
            listing_data.user = request.user
            print(listing_data)
            listing_data.save()
            
            #input bid form with initial bid.
            Bids.objects.create(user_id=request.user, listing_id=listing_data, bid_amount=listing_data.starting_bid, initial_bid=True)
            return HttpResponseRedirect(reverse("index"))

    return render (request, "auctions/create.html", {
        "form": ListingForm
    })

def listing(request, title):
    print("in listing.view")
    listing_data = Listing.objects.get(title=title)
    if request.method == "POST":
        print("check if listing is in post")
        bidForm = BidForm(request.POST)
        if bidForm.is_valid:
            bid_data = bidForm.save(commit=False)
            if (bid_data.bid_amount > listing_data.starting_bid):
                print("amount entered is bigger")
                #money conversion
                bid_data.bid_amount = "{:,.2f}".format(bid_data.bid_amount) 
                bid_data.user_id = request.user
                bid_data.listing_id = listing_data
                bid_data.initial_bid = False
                bid_data.save()
                return render(request, "auctions/listing.html", {
                    "bid_data": bid_data,
                    "bidForm":BidForm,
                    "listing":listing_data
                })
    print ("Starting List View")
    print(f"Title: {title}")
    print(listing_data)
    bid_data = Bids.objects.filter(listing_id = listing_data).last()
    return render(request, "auctions/listing.html", {
        "bid_data": bid_data,
        "bidForm": BidForm,
        "listing": listing_data
    })

def add_watchlist(request, listing_id):
    print("in watchlist")
    listing_data = Listing.objects.get(pk=listing_id)
    print(listing_data)
    listing_data.watchlist.add(request.user)
    print(f"{request.user} has added {listing_data.title} to the watchlist")
    return HttpResponseRedirect(reverse("listing", kwargs={'title':listing_data.title}))

def categories(request):
    print("In categories")
    #create a list of categories
    category_list=[]
    for category in CATEGORIES:
        category_list.append(category[0])
    
    return render(request, "auctions/categories.html",{
        "categories":category_list
    })

def category(request, category):
    category_entries = Listing.objects.filter(category=category)
    print(category_entries)

    return render(request, "auctions/category.html",{
        "category": category,
        "listings":category_entries
    })