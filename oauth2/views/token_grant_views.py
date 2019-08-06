import time

from django.http import HttpResponse
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from eth3.contracts.client_management_deployment import ClientManagementContract, ClientSummary
from eth3.contracts.notification_deployment import NotificationContract
from eth3.web3_client import Web3Client
from fcm.notification import FcmCover, FcmMessage, send_fcm_notification
from oauth2.locker import Locker
from oauth2.memory import AuthProcessParameter, ParameterCache, AuthCodeCache
from oauth2.secret_generator import random_string, random_string_digits


@method_decorator(csrf_exempt, name='dispatch')
def access_token(request):
    """
    parameter로 정상적인 값이 입력되었는지 확인.
    Client <-> Proxy 사이의 통신.
    """
    try:
        grant_type = request.POST['grant_type']
        client_id = request.POST['client_id']
        client_secret = request.POST['client_secret']
        code = request.POST['code']
    except KeyError:
        return HttpResponse(status=400, content='parameter unfulfilled')

    email = AuthCodeCache.get_value(code)

    web3c = Web3Client()
    n_contract = NotificationContract(web3c)
    device_token = n_contract.get_device_token(email)

    cm_contract = ClientManagementContract(web3c)
    summary: ClientSummary = cm_contract.get_client_summary(client_id)
    permissions = summary.scopes

    # 사용자에게 code와 state를 전송하고 access_token을 응답받는다.
    # 사용자 승락/거절 응답을 대기
    temporary_id = random_string()
    data = {
        'type': 'access_token',
        'client_id': client_id,
        'unlock_code': temporary_id,
        'code': code,
    }
    req_message = FcmMessage(device_token, FcmCover(title='', body=''), data)
    send_fcm_notification(req_message)
    Locker.register(temporary_id)
    count = 0
    while count != 20:
        time.sleep(1)
        count += 1
        token = Locker.storage[temporary_id]
        if token is not None:
            break
    if token is False or count == 20:
        return HttpResponse('access denied')

    context = {
        'access_token': token['access_token'],  # random_string_digits(32),
        'token_type': token['Bearer'],  # "Bearer",
        "expires_in": token['expires_in'],  # 3600,
        "scopes": token['scopes'],  # permissions,
        "refresh_token": token['refresh_token'],  # random_string_digits(32)
        "redirect_url": token['redirect_url']
    }
    access_token = token['access_token']
    token_type = token['token_type']
    expires_in = token['expires_in']
    scopes = token['scopes']
    refresh_token = token['refresh_token']
    redirect_url = token['redirect_url']

    request.session[access_token] = email

    redirect_to = f"{redirect_url}?" \
        f"access_token={access_token}&token_type={token_type}&expires_in={expires_in}&" \
        f"scopes={scopes}&refresh_token={refresh_token}"
    return redirect(redirect_to)


def fcm_access_token(request):
    try:
        reply = request.GET['reply']
        unlock_code = request.GET['unlock_code']
    except Exception:
        pass
    Locker.storage[unlock_code] = reply
    return HttpResponse('')
