from django.contrib.auth.models import AbstractUser
from django.db import models
from django.forms import ModelForm
from django.forms.widgets import TextInput, Textarea

CATEGORIES = [
    ("Motors", "Motors"),
    ("Fashion", "Fashion"),
    ("Electronics", "Electronics"),
    ("Collectibles and Art", "Collectibles & Art"),
    ("Home and Garden", "Home & Garden"),
    ("Sporting Goods", "Sporting Goods"),
    ("Toys", "Toys"),
    ("Business and Industrial", "Business & Industrial"),
    ("Music", "Music")
]
class User(AbstractUser):
    pass
class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=300)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,null=True
    )
    starting_bid = models.DecimalField(
        max_digits=10,
        decimal_places=2)
    image = models.URLField(blank=True)
    category =  models.CharField(
        max_length=25,
        choices=CATEGORIES
    )
    watchlist = models.ManyToManyField(User, blank=True, related_name="watchlist")
    def __str__(self):
        return f"{self.title} created by {self.user} starting at {self.starting_bid}"
class Bids(models.Model):
    user_id = models.ForeignKey(
        User, on_delete=models.CASCADE,null=True
    )
    listing_id= models.ForeignKey(
        Listing, on_delete=models.CASCADE,null=True
    )
    bid_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    initial_bid = models.BooleanField(null=True)

    def __str__(self):
        return f"Created by {self.user_id} for listing {self.listing_id} with bid amount {self.bid_amount}"
    

class Comments(models.Model):
    listing_id = models.IntegerField
    user_id = models.IntegerField
    value = models.CharField(max_length=300)

class ListingForm(ModelForm):
    class Meta:
        model = Listing
        fields = ['title','description','starting_bid', 'image', 'category']
        widgets = {
            'description': Textarea(attrs={"rows":15, "cols":100}),
            'image': TextInput(attrs={"size":100})
        }

class BidForm(ModelForm):
    class Meta:
        model = Bids
        fields = ['bid_amount']