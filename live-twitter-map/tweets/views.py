from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
import json
from . import models
from datetime import datetime
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
def startup(request):
    # t = int((time.time()-60)*1000)
    # messages = models.Tweet.objects.filter(timestmap_ms__gt=t)
    return JsonResponse({"message": "test"})
