from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required



def index(request):
    return HttpResponse("Hello, World. You're the polls index.")

@login_required
def portfolio(request):
    user = request.user
    return HttpResponse("{0}, você está logado.".format(user.first_name))

# Create your views here.
