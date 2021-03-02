from django.urls import path

from tweets import views

urlpatterns = [
    path('', views.map, name='index'),
    path('health/',views.health)
    # path('test/', views.test, name='test')
]
