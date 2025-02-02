from django.urls import path
from . import views

urlpatterns = [
    path('', views.map, name='map'),
    path('navigate/', views.navigate, name='navigate'),
    path('calculatedPoints/', views.calculatedPoints, name='calculatedPoints'),
]
