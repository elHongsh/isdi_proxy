from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from oauth2.secret_generator import random_string_digits


def register_page(request):
    # 사용자가 제시한 값이 맞는지 확인한다. (right tx-data?)
    context = {'client_id': random_string_digits(32)}
    return render(request, 'registration_page.html', context=context)


@method_decorator(csrf_exempt, name='dispatch')
def client_secret_assignment(request):
    try:
        client_id = request.POST['client']
    except KeyError:
        pass

    context = {'client_secret': random_string_digits(32)}
    return JsonResponse(data=context, json_dumps_params={'ensure_ascii': False})


@method_decorator(csrf_exempt, name='dispatch')
def register(request):
    try:
        client_name = request.POST['client_name']
        client_public_key = request.POST['client_public_key']
        client_scopes = request.POST.getlist('permissions')
    except KeyError:
        return HttpResponse(status=400, content='wrong input')

    client_id = random_string_digits(32)
    client_secret = random_string_digits(32)

    context = {
        'client_name': client_name,
        'client_id': client_id,
        'client_secret': client_secret,
        'client_public_key': client_public_key,
        'client_scopes': client_scopes
    }
    return render(request, 'registration_result.html', context)


def register_done(request):
    client_name = 'name'
    client_scopes = 'scopes'
    client_id = 'id'
    client_secret = 'secret'
    client_public_key = 'pubKey'

    data = {
        'clientName': client_name
    }
