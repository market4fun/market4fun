from django.db import models
from django.contrib.auth.models import AbstractUser,UserManager
from ibroker.models import Order,Quote
from django.db.models import Sum


# Create your models here.
INITIAL_CASH = 100000
class CustomUserManager(UserManager):
    pass

class CustomUser(AbstractUser):

    cash = models.DecimalField(max_digits=15,decimal_places=2,default=100000)
    objects = CustomUserManager()


    def get_amount_cash(self):
        orders = Order.objects.filter(order_user=self)
        deltaCash = 0
        for order in orders:
            deltaCash+=order.order_stock_quote.price*order.order_amount



        return INITIAL_CASH+deltaCash


    def get_user_total_assets_value_date(self,date):
        assetsValue =0

        stockAmount = Order.objects.filter(order_user=self).values('order_stock_quote__stock','order_amount',).annotate(Sum('order_amount'))

        for pair in stockAmount:
            current_price = Quote.objects.filter(stock=pair[0]).filter(quote_datetime__lte=date).order_by('-quote_datetime')[0].price

            assetsValue+=current_price*pair[1]



        return assetsValue+self.get_amount_cash()




