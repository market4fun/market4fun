from django.db import models
from users.models import CustomUser
from django import forms
from django.contrib import admin
TOTAL_DIGITS = 15

# Create your models here.

class Company(models.Model):
    company_name = models.CharField(max_length=200)
    company_description = models.CharField(max_length=255)
    company_img_url = models.URLField() #TODO trocar para ImageField
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    state = models.CharField(max_length=200)
    country = models.CharField(max_length=200)

    def __str__(self):
        return self.company_name

class Stock(models.Model):
    stock_code = models.CharField(max_length=50)
    stock_description = models.CharField(max_length=200)
    company = models.ForeignKey(Company,on_delete=models.CASCADE)

    def __str__(self):
        return self.stock_code

class Quote(models.Model):
    stock = models.ForeignKey(Stock,on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=TOTAL_DIGITS,decimal_places=2)
    quote_datetime = models.DateTimeField('Data da cotação')

    def __str__(self):
        return "{0} - {1}".format(self.stock,self.quote_datetime)


class Order(models.Model):
    order_amount = models.IntegerField()
    order_stock_quote = models.ForeignKey(Quote,on_delete=models.DO_NOTHING)
    order_datetime = models.DateTimeField()
    order_user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)

    def __str__(self):
        return "{0} - {1} - {2}".format(self.order_user.first_name,self.order_stock_quote.stock.stock_code,self.order_datetime)

