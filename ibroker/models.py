from django.db import models
from django import forms
from django.contrib import admin
from users.models import CustomUser
from django.db.models import Sum,F
import datetime
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


    def get_price_date(self,datetime):
        price = Quote.objects.filter(stock=self).filter(quote_datetime__lte=datetime).order_by('-quote_datetime')[0].price
        return price
    @property
    def get_price_now(self):
        price = Quote.objects.filter(stock=self).filter(quote_datetime__lte=datetime.datetime.now()).order_by('-quote_datetime')[0].price
        return price

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

class PorfolioItem():
    def __init__(self,stock_code,amount,invested_value,current_price):
        self.stock_code = stock_code
        self.amount = amount
        self.invested_value = invested_value
        self.current_price = current_price

        self.current_value = current_price*amount



class UserHistory():

    def get_amount_cash(self,user,date=None):

        orders = Order.objects.filter(order_user=user)
        if date is not None:
            orders = orders.filter(order_datetime__lte=date)

        deltaCash = 0
        for order in orders:
            deltaCash+=order.order_stock_quote.price*order.order_amount

        return CustomUser.INITIAL_CASH-deltaCash


    def get_user_total_assets_value_date(self,user,date):
        assetsValue =0

        stockAmount = Order.objects.filter(order_user=user).filter(order_datetime__lte=date).values(stock=F('order_stock_quote__stock_id')).annotate(total_amount=Sum('order_amount'))

        for pair in stockAmount:
            current_price = Quote.objects.filter(stock=pair['stock']).filter(quote_datetime__lte=date).order_by('-quote_datetime')[0].price

            assetsValue+=current_price*pair['total_amount']



        return  assetsValue+self.get_amount_cash(user,date)




