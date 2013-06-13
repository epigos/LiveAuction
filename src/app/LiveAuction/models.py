from django.db import models
from django.contrib.auth.models import User

class Auction(models.Model):
	Id = models.AutoField(primary_key=True)
	Title = models.CharField(max_length=100, blank=False)
	Description = models.CharField(max_length=250, null=True, blank=True)
	Hour = models.DateTimeField(auto_now=False)

class Bid(models.Model):
	Id = models.AutoField(primary_key=True)
	Auction = models.ForeignKey(Auction)
	User = models.ForeignKey(User)
	Amount = models.DecimalField(max_digits=12, decimal_places=2)
	Hour = models.DateTimeField(auto_now=True)

