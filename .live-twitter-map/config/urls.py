from django.contrib import admin
from django.urls import path
from django.conf.urls import include
# from ws import views
from tweets import views
urlpatterns = [
    # path('admin/', admin.site.urls),
    # path('accounts/', include("django.contrib.auth.urls")),
    # path('api/', include('ws.urls')),
    # path('health', views.health, name='health'),
    # path('', views.index, name='home'),
    # path('tweets/', views.index, name='home'),
    path('', views.map, name='map'),
    # path('test/', views.test, name='test')
]
