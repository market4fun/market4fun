from django.shortcuts import render,redirect
from django.shortcuts import Http404
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.template import loader
from django.contrib import messages
from django.urls import reverse
from django.views import generic
from django.views.generic import TemplateView,ListView
from ibroker.models import Company, Stock, UserHistory,CustomUser
from ibroker.models import Quote,Order, PorfolioItem
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
import datetime
import json
# Create your views


class HomePageView(TemplateView):
    template_name = 'index/home.html'
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)

        users = CustomUser.objects.all()
        ctx = {}
        qtd_usuarios = 0

        dates = Quote.objects.values_list('quote_datetime').distinct().order_by('quote_datetime')

        dates = [d[0].date().__str__() for d in dates]



        for user in users:
            qtd_usuarios+=1
            ctx[user] = {}

            perfs = [float(UserHistory().get_user_total_assets_value_date(user, d)) for d in dates]

            ctx[user] = {
                'dates': json.dumps(dates),
                'perfs': json.dumps(perfs),
                'atual': perfs[len(perfs)-1]
            }





        context['ctx'] = ctx
        context['qtd_usuarios'] = qtd_usuarios
        return context