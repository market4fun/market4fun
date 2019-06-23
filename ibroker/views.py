from django.shortcuts import render
from django.shortcuts import Http404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.template import loader
from django.views import generic
from django.views.generic import TemplateView
from ibroker.models import Company
from ibroker.models import Quote
from .forms import UploadQuotesFile
from .forms import NameForm
from django.views import View
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


class Order(View):
    def get(request):
        user = request.user
        try:
            last_update_datetime = Quote.objects.order_by('quote_datetime')[0].quote_datetime
        except:
            raise Http404("Não existe nenhuma cotação ainda.")

        quote_list = Quote.objects.filter(quote_datetime__gte=last_update_datetime)
        context = {
            'quote_list': quote_list,
        }
        return render(request, 'ibroker/order/order.html', context)

    def post(request):
        user = request.user

        return HttpResponse("{0}, você comprou )")

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


@login_required
def stocks(request):
    return HttpResponse("Página para visualizar as ações listadas.")





