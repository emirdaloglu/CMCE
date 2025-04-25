from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('add-recipe/', views.add_recipe, name='add_recipe'),
    path('corbalar/', views.corbalar, name='corbalar'),
    path('et-yemekleri/', views.et_yemekleri, name='et_yemekleri'),
    path('favorites/', views.favorites, name='favorites'),
    path('history/', views.history, name='history'),
    path('calculate/with-cost', views.calculate_with_cost, name='calculate_with_cost'),
]