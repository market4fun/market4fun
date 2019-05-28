from django.urls import path


from . import views

app_name = 'ibroker'
urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path('portfolio',views.portfolio,name='portfolio')
]