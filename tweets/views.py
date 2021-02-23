from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'tweets/index.html', {})


def map(request):
    return render(request, 'tweets/map.html')
# test reload 
def test(request):
    return render(request, 'tweets/tweet_pin_test.html')