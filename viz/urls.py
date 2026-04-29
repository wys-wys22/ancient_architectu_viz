from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('api/chart-data/', views.chart_data_api, name='chart_data_api'),
]