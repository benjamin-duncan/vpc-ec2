from django.urls import path

from tweets import views

urlpatterns = [
    path('', views.map, name='index'),
    # path('test/', views.test, name='test')
]
