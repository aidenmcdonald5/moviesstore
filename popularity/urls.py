from django.urls import path
from . import views
urlpatterns = [
    path('', views.popularity_map, name='popularity.map'),
]

