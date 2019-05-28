from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from django.views import generic
from django.views.generic import TemplateView
from ibroker.models import Company

# Create your views here.

class HomePageView(TemplateView):
    template_name = 'home.html'



# Visualização da carteira do usuario
@login_required
def portfolio(request):
    user = request.user
    return HttpResponse("{0}, você está logado. Página de portfolio".format(user.first_name))


# Executar ordens
@login_required
def order(request):
    user = request.user
    return HttpResponse("{0}, você está na página de execução de ordens (compra e venda)")

# Visualizar cotações
def quotes(request):
    return HttpResponse("Página para visualizar cotações")

# visualizar histórico de operações
@login_required
def history(request):
    return HttpResponse("Página para visualizar histórico de operações.")


class CompaniesView(generic.ListView):
    template_name = 'ibroker/companies.html'
    context_object_name = 'company_list'

    def get_queryset(self):
        return Company.objects

def companies(request):
    return HttpResponse("Página para visualizar as companhias listadas.")

def stocks(request):
    return HttpResponse("Página para visualizar as ações listadas.")





