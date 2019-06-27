from django.shortcuts import render,redirect
from django.shortcuts import Http404
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.template import loader
from django.contrib import messages
from django.urls import reverse
from django.views import generic
from django.views.generic import TemplateView,ListView
from ibroker.models import Company, Stock
from ibroker.models import Quote,Order, PorfolioItem
from .forms import UploadQuotesFile,OrderForm,SellForm
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
import datetime

# Create your views here.
class HomePageView(TemplateView):
    template_name = 'home.html'

#region Companhias
class CompaniesView(generic.ListView):
    template_name = 'ibroker/company/companies.html'
    context_object_name = 'company_list'

    def get_queryset(self):
        return Company.objects.all


class CompanyDetail(generic.DetailView):
    model = Company
    template_name = 'ibroker/company/detail.html'
#endregion



def upload_file(request):
    if request.method=="POST":
        form = UploadQuotesFile(request.POST,request.FILES)

        if form.is_valid():
            #handle_upload_file(request.FILES['file'])
            return HttpResponse('Arquivo enviado com sucesso')
    else:
        form = UploadQuotesFile()
        return render(request,'upload.html',{'form':form})

@method_decorator(login_required, name='dispatch')
class OrderView(View):
    def get(self,request):
        user = request.user

        form = OrderForm(user=user)

        return render(request, 'ibroker/order/order.html', {'form':form,'user':user})

    def post(self,request):
        user = request.user

        #Aqui a mágica acontece
        form = OrderForm(request.POST,user=user)

        if(form.is_valid()):
            try:
                qtd = form.cleaned_data['qtd'];
                stockId = form.cleaned_data['stock']
                stock = Stock.objects.get(pk=stockId)
                quote = Quote.objects.filter(stock = stock.id).order_by('-quote_datetime')[0]


                now = datetime.datetime.now()

                newOrder = Order(order_amount=qtd,order_stock_quote=quote,order_datetime=now,order_user=user)
                newOrder.save()

                total = quote.price*qtd
                user.cash=user.cash-total
                user.save()


                messages.success(request,"Ordem executada com sucesso")

                return HttpResponseRedirect(reverse("ibroker:portfolio"))
            except:
                raise Http404("Erro ao executar ordem.")

        return render(request, 'ibroker/order/order.html', {'form':form,'user':user})



# Visualização da carteira do usuario - possibilidade de vender
@login_required
def portfolio(request):
    user = request.user
    ctx = {}

    #
    # ctx = Order.objects.raw(''' SELECT t3.stock_code,
    # sum(t1.order_amount) as amount,  sum(t1.order_amount*t2.price) as spent
    # FROM ibroker_order as t1
    # JOIN ibroker_quote as t2
    # ON t1.order_stock_quote_id=t2.id
    # JOIN ibroker_stock as t3 ON t2.stock_id=t3.id group by t3.id ''')

    ordersFromUser = Order.objects.filter(order_user = user)


    stocksDic = {}

    for order in ordersFromUser:
        quote = order.order_stock_quote
        stock = quote.stock

        if not stock.id in stocksDic:
            invested_value= order.order_amount*quote.price


            current_price = Quote.objects.filter(stock=stock.id).order_by('-quote_datetime')[0].price

            item = PorfolioItem(stock.stock_code,order.order_amount,invested_value,current_price)

            stocksDic[stock.id] = item

        else:
            stocksDic.get(stock.id).amount += order.order_amount
            stocksDic.get(stock.id).invested_value += order.order_amount * quote.price
            stocksDic.get(stock.id).current_value = stocksDic.get(stock.id).amount * stocksDic.get(stock.id).current_price



    return render(request,'ibroker/portfolio.html',{'dic':stocksDic})



@method_decorator(login_required, name='dispatch')
class SellView(View):
    def get(self,request):
        user = request.user

        form = SellForm(user=user)

        return render(request, 'ibroker/order/sell.html', {'form':form,'user':user})

    def post(self,request):
        user = request.user

        #Aqui a mágica acontece2
        form = SellForm(request.POST,user=user)

        if(form.is_valid()):
            try:
                qtd = form.cleaned_data['qtd'];
                stockId = form.cleaned_data['stock']
                stock = Stock.objects.get(pk=stockId)
                quote = Quote.objects.filter(stock = stock.id).order_by('-quote_datetime')[0]


                now = datetime.datetime.now()

                newOrder = Order(order_amount=-qtd,order_stock_quote=quote,order_datetime=now,order_user=user)
                newOrder.save()

                total = quote.price*qtd
                user.cash=user.cash+total
                user.save()


                messages.success(request,"Ordem executada com sucesso")

                return HttpResponseRedirect(reverse("ibroker:portfolio"))
            except:
                raise Http404("Erro ao executar ordem.")

        return render(request, 'ibroker/order/order.html', {'form':form,'user':user})












# Visualizar cotações
def quotes(request):
    return HttpResponse("Página para visualizar cotações")

@method_decorator(login_required,name='dispatch')
class HistoryView(View):


    def get(self,request):
        user = request.user




        dates = Quote.objects.distinct('quote_datetime')







        return HttpResponse("Página para visualizar histórico de operações.")


class StockListView(ListView):
    model = Stock
    context_object_name = "stocks"
    template_name = 'ibroker/stock/stocks.html'

class StockDetailView(generic.DetailView):
    model = Stock
    template_name = 'ibroker/stock/detail.html'


@login_required
def stocks(request):
    return HttpResponse("Página para visualizar as ações listadas.")





