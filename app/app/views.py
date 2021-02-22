from app.settings import HELLO_WORLD
from django.http import HttpResponse
def hello(request):
    response = f"<html><body>{HELLO_WORLD}</body></html>"
    return HttpResponse(response)

def health(request):
    return HttpResponse()