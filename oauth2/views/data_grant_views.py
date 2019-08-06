import json

from django.http import HttpResponse, JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from eth3.contracts.client_management_deployment import ClientManagementContract, ClientSummary
from eth3.contracts.notification_deployment import NotificationContract
from eth3.web3_client import Web3Client
from fcm.notification import FcmMessage, FcmCover, send_fcm_notification
from oauth2.locker import Locker
from oauth2.secret_generator import random_string


@method_decorator(csrf_exempt, name='dispatch')
def get_data(request):
    try:
        client_id = request.POST['client_id']
        client_secret = request.POST['client_secret']
        access_token = request.POST['access_token']
        email = request.session[access_token]
    except Exception:
        HttpResponse('wrong parameters')
    web3c = Web3Client()
    n_contract = NotificationContract(email)
    token = n_contract.get_device_token(email)

    cm_contract = ClientManagementContract(web3c)
    summary: ClientSummary = cm_contract.get_client_summary(client_id)

    temporary_id = random_string()
    data = {
        'type': 'data',
        'client_id': client_id,
        'access_token': access_token,
        'unlock_code': temporary_id,
    }
    message = FcmMessage(receiver=token, cover=FcmCover('', ''), data=data)
    send_fcm_notification(message)

    return JsonResponse(content=received_data)


def fcm_get_data(request):
    json_string = request.body.decode('utf-8')
    json_object = json.loads(json_string)
    data = json_object['data']
    unlock_code = json_object['unlock_code']
    Locker.storage[unlock_code] = json_object['data']
