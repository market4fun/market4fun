from django.urls import path


from . import views

app_name = 'ibroker'
urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path('portfolio', views.portfolio, name='portfolio'),
    path('companies', views.CompaniesView.as_view(), name='companies'),
    path('companies/<slug:pk>/', views.CompanyDetail.as_view(), name='company_detail'),
    path('stocks/', views.StockListView.as_view(), name='stocks'),
    path('stocks/<slug:pk>', views.StockDetailView.as_view(), name='stock_detail'),
    path('order/', views.OrderView.as_view(), name='order'),
    path('sell/', views.SellView.as_view(), name='sell'),
    path('history/', views.HistoryView.as_view(), name='history'),

]