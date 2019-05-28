from django.db import models
from django.contrib.auth.models import AbstractUser

TOTAL_DIGITS = 15

# Create your models here.


class CustomUser(AbstractUser):

    def __str__(self):
        return self.email


class Address(models.Model):
    address_street = models.CharField(max_length=200)
    address_city = models.CharField(max_length=200)
    address_state = models.CharField(max_length=200)
    address_country = models.CharField(max_length=200)

class Company(models.Model):
    company_name = models.CharField(max_length=200)
    company_description = models.CharField(max_length=255)
    company_img_url = models.URLField() #TODO trocar para ImageField
    address = models.ForeignKey(Address,on_delete=models.CASCADE)

class Stock(models.Model):
    stock_code = models.CharField(max_length=50)
    stock_description = models.CharField(max_length=200)
    company = models.ForeignKey(Company,on_delete=models.CASCADE)

class Quote(models.Model):
    stock = models.ForeignKey(Stock,on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=TOTAL_DIGITS,decimal_places=2)
    quote_datetime = models.DateTimeField('Data da cotação')


class Order(models.Model):
    #BUY = 'B'
    #SELL = 'S'
    #ORDER_TYPES = [(BUY,"Compra"),(SELL,"Venda")]
    #order_type = models.CharField(max_length=1,choices=ORDER_TYPES,default=BUY)
    order_amount = models.IntegerField()
    order_price = models.DecimalField(max_digits=TOTAL_DIGITS,decimal_places=2)
    order_datetime = models.DateTimeField()
    order_user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)


#Todo criar esta view no banco de dados.

# class SimplifiedPortfolio (models.Model):
#     portfolio_stock = models.ForeignKey(Stock,on_delete=models.CASCADE)
#     portfolio_amount = models.IntegerField()
#     portfolio_mean_price = models.DecimalField(max_digits=TOTAL_DIGITS, decimal_places=2)
#     portfolio_current_price = models.DecimalField(max_digits=TOTAL_DIGITS, decimal_places=2)
#     portfolio_total_mean_price = models.DecimalField(max_digits=TOTAL_DIGITS,decimal_places=2)
#     portfolio_total_current_price = models.DecimalField(max_digits=TOTAL_DIGITS, decimal_places=2)
#     portfolio_pl = models.DecimalField(max_digits=TOTAL_DIGITS, decimal_places=2)
#
#     class Meta:
#         managed = False;
#         db_table='simplified_portfolio_view'