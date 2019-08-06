from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from oauth2.locker import Locker


def index(request):
    return render(request, 'index_did.html')


def notification_response(request):
    try:
        unlock_code = request.GET['unlock_code']
        access = request.GET['access']
    except KeyError:
        return HttpResponse(status=400)
    if access == 'true':
        access = True
    else:
        access = False

    Locker.storage[int(unlock_code)] = access
    return HttpResponse(status=200, content='accepted')
