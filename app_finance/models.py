from django.db import models
from django.contrib.auth.models import User



class Customer(models.Model):
	user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
	name = models.CharField(max_length=200, null=True)
	email = models.CharField(max_length=200, null=True,blank=True)
	date_created = models.DateTimeField(auto_now_add=True, null=True)




class Finance(models.Model):
	expenses_category = [
	    ("Saving", "Saving"),
	    ("Food", "Food"),
	    ("Bills", "Bills"),
	    ("Rent", "Rent"),
	    ("Extra", "Extra"),
	]

	expenses_month = [
	    ("01", "January"),
	    ("02", "February"),
	    ("03", "March"),
	    ("04", "April"),
	    ("05", "May"),
	    ("06", "June"),
	    ("07", "July"),
	    ("08", "August"),
	    ("09", "September"),
	    ("10", "October"),
	    ("11", "November"),
	    ("12", "December"),
	]

	customer = models.ForeignKey(User, on_delete=models.CASCADE, null=True,blank=True)
	category = models.CharField(choices=expenses_category, max_length=200)
	price = models.IntegerField()
	month = models.CharField(choices=expenses_month, max_length=200)
