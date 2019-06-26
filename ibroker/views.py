from django.shortcuts import render
from django.shortcuts import Http404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.template import loader
from django.views import generic
from django.views.generic import TemplateView,ListView
from ibroker.models import Company, Stock
from ibroker.models import Quote
from .forms import UploadQuotesFile,OrderForm
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
            handle_upload_file(request.FILES['file'])
            return HttpResponse('Arquivo enviado com sucesso')
    else:
        form = UploadQuotesFile()
        return render(request,'upload.html',{'form':form})

@method_decorator(login_required, name='dispatch')
class Order(View):
    def get(self,request):
        user = request.user
        # try:
        #     last_update_datetime = Quote.objects.order_by('quote_datetime')[0].quote_datetime
        # except:
        #     raise Http404("Não existe nenhuma cotação ainda.")
        #
        # quote_list = Quote.objects.filter(quote_datetime__gte=last_update_datetime)
        # context = {
        #     'quote_list': quote_list,
        # }
        #
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


#                 order = Order(order_amount=qtd,order_stock_quote=quote,order_datetime=datetime.datetime.now(),order_user=user)
# #                order.save()
#
#
#                 #user.cash=user.cash-total
#                 # user.save()



                return HttpResponse(
                    "Stock: {0}<br>Preço: {1}<br>Total:{2}".format(stock.stock_code,quote.price,quote.price*qtd))
            except:
                raise Http404("Erro ao executar ordem.")

        return render(request, 'ibroker/order/order.html', {'form':form,'user':user})



def handle_upload_file(file):
    a = "teste"


# Visualização da carteira do usuario - possibilidade de vender
@login_required
def portfolio(request):
    user = request.user
    return HttpResponse("{0}, você está logado. Página de portfolio".format(user.first_name))




# Visualizar cotações
def quotes(request):
    return HttpResponse("Página para visualizar cotações")

# visualizar histórico de operações
@login_required
def history(request):
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





