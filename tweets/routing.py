from django.urls import re_path

from tweets import consumers

websocket_urlpatterns = [
    re_path(r'ws/tweets/$', consumers.TweetsConsumer),
]
