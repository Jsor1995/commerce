from django.contrib.auth import authenticate, login, logout
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Listing, ListingForm

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
            return HttpResponseRedirect(reverse("index"))


    return render (request, "auctions/create.html", {
        "form": ListingForm
    })

def listing(request, title):
    listing_data = Listing.objects.get(title=title)
    print(listing_data)
    return render(request, "auctions/listing.html",{
        "listing": listing_data
    })
