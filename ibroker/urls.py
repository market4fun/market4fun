from django.urls import path


from . import views

app_name = 'ibroker'
urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path('portfolio', views.portfolio, name='portfolio'),
    path('companies', views.CompaniesView.as_view(), name='companies'),
    path('companies/<slug:pk>/', views.CompanyDetail.as_view(), name='company_detail'),
    path('order/', views.order, name='order'),

]