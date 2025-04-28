from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('add-recipe/', views.add_recipe, name='add_recipe'),
    path('corbalar/', views.corbalar, name='corbalar'),
    path('et-yemekleri/', views.et_yemekleri, name='et_yemekleri'),
    path('favorites/', views.favorites, name='favorites'),
    path('history/', views.history, name='history'),

    
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    path('calculate/with-cost', views.calculate_with_cost, name='calculate_with_cost'),
    path('add-to-favorites/', views.add_to_favorites, name='add_to_favorites'),
    path('remove-favorite/', views.remove_favorite, name='remove_favorite'),

]