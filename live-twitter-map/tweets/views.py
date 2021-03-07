from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
import json
from . import models
from datetime import datetime
import time
from . import serializers
from rest_framework.response import Response
from rest_framework.decorators import api_view
# Create your views here.
def index(request):
    return render(request, 'tweets/index.html', {})


def map(request):
    return render(request, 'tweets/map.html')
# test reload 
def test(request):
    return render(request, 'tweets/tweet_pin_test.html')

def health(request):
    return HttpResponse()

# get tweets from previous minute
@api_view(['GET'])
def startup(request):
    t = int((time.time()-60)*1000)

    offset = 20

    messages = models.Tweet.objects.filter(timestamp_ms__gt=t-20000,timestamp_ms__lt=t+40000)
    serializer = serializers.StartupSerializer(messages, many=True)
    return Response(serializer.data)

