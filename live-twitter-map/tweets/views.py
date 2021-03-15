from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from django.db.models import Min
import json
from . import models
from datetime import datetime
import time
from . import serializers
from rest_framework.response import Response
from rest_framework.decorators import api_view
# Create your views here.
from enum import Enum

# class _Time():
#     def second(self): return 
#     def minute(self): return self.second()*60
#     def hour(self): return self.minute()*60
#     def day(self): return self.hour()*24
#     def now(self): return int(time.time()*1000)


def index(request):
    return render(request, 'tweets/index.html', {})


def map(request):
    return render(request, 'tweets/map.html')
# test reload 
def test(request):
    return render(request, 'tweets/tweet_pin_test.html')

def health(request):
    return HttpResponse()

def request_timestamp():
    return int((time.time())*1000)

_time={
    "second": 1000,
    "minute": 60000,
    "hour": 3600000,
    "day": 86400000,
}

# get tweets from previous minute
@api_view(['GET'])
def startup(request):
    t=request_timestamp()
    messages = models.Tweet.objects.filter(timestamp_ms__gt=t-60000,timestamp_ms__lt=t)
    serializer = serializers.StartupSerializer(messages, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def stats(request):
    t=request_timestamp()
    day_query = models.Tweet.objects.filter(timestamp_ms__gt=t-_time["day"])
    instance = {
        "total": models.Tweet.objects.count(),
        "day": day_query.count(),
        "hour": day_query.filter(timestamp_ms__gt=t-_time["hour"]).count(),
        "minute": day_query.filter(timestamp_ms__gt=t-_time["minute"]).count()
    }

    serializer = serializers.StatsSerializer(instance)
    return Response(serializer.data)

def query_range(query,_min,_max):
    if query < _min: return _min
    elif query > _max: return _max
    else: return query

@api_view(['GET'])
def graph(request):
    # 10 seconds 50 vals
    t=request_timestamp()
    min = models.Tweet.objects.aggregate(Min("timestamp_ms"))["timestamp_ms__min"]

    diff=query_range(
        int(request.query_params.get('diff',1)),
        1,
        60,)

    delta=query_range(
        _time[f"{request.query_params.get('t','minute')}"]*diff,
        _time["second"],
        _time["day"],)

    length=query_range(int(request.query_params.get("n",50)),10,100)
    data = []
    for i in range(length):
        if min > t-(i+1)*delta and i > 0: break

        data.append({
            "t": t-i*delta,
            "y": models.Tweet.objects.filter(timestamp_ms__lt=t-i*delta,timestamp_ms__gt=t-(i+1)*delta).count()
        })
        

    # data.update({
    #     "delta_t"= delta, 
    # })

    return Response(data)

# @api_view(['GET'])
# def graph(request):
#     data=request.query_params['t']
#     s=_time[f"{request.query_params['t']}"]
#     return HttpResponse(f"<body>{s}</body>")