from django.shortcuts import render
from django.shortcuts import Http404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.template import loader
from django.views import generic
from django.views.generic import TemplateView
from ibroker.models import Company
from ibroker.models import Quote


# Create your views here.

class HomePageView(TemplateView):
    template_name = 'home.html'




# Visualização da carteira do usuario
@login_required
def portfolio(request):
    user = request.user
    return HttpResponse("{0}, você está logado. Página de portfolio".format(user.first_name))


# Aqui mostra as opções para executar. (Ações e seus preços)
@login_required
def order_index(request):
    return HttpResponse("{0}, você comprou )")


# Aqui executa. (Após o post)
@login_required
def order(request):
    if request.method!="POST":
        user = request.user
        try:
            last_update_datetime = Quote.objects.order_by('quote_datetime')[0].quote_datetime
        except:
            raise Http404("Não existe nenhuma cotação ainda.")


        quote_list = Quote.objects.filter(quote_datetime__gte=last_update_datetime)
        context = {
            'quote_list': quote_list,
        }
        return render(request,'ibroker/order/order.html',context)

    else:
        user = request.user

        return HttpResponse("{0}, você comprou )")


# Visualizar cotações
def quotes(request):
    return HttpResponse("Página para visualizar cotações")

# visualizar histórico de operações
@login_required
def history(request):
    return HttpResponse("Página para visualizar histórico de operações.")


class CompaniesView(generic.ListView):
    template_name = 'ibroker/company/companies.html'
    context_object_name = 'company_list'

    def get_queryset(self):
        return Company.objects.all


class CompanyDetail(generic.DetailView):
    model = Company
    template_name = 'ibroker/company/detail.html'


def stocks(request):
    return HttpResponse("Página para visualizar as ações listadas.")





