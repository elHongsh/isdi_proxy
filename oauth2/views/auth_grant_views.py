import time

from django.http import HttpResponse
from django.shortcuts import redirect

from eth3.contracts.client_management_deployment import ClientManagementContract, ClientSummary
from eth3.contracts.notification_deployment import NotificationContract
from eth3.web3_client import Web3Client
from fcm.notification import send_fcm_notification, FcmMessage, FcmCover
from oauth2.locker import Locker
from oauth2.memory import AuthCodeCache, ParameterCache, AuthProcessParameter
from oauth2.secret_generator import random_string


def authorize(request):
    """ auth-code를 사용자에게 요청"""
    try:
        client_id = request.GET['client_id']
        response_type = request.GET['response_type']
        redirect_url = request.GET['redirect_url']
        response_mode = request.GET['response_mode']
        state = request.GET['state']
    except KeyError:
        return HttpResponse(status=400, content='parameter unfulfilled.')

    # 서버가 제공한 state 값을 사용자가 제시했는지 비교하여 CSRF를 방지한다.
    pass

    # 사용자의 로그인 여부를 확인한다.
    if not request.session.has_key('email'):
        key = random_string()
        temporal_value = AuthProcessParameter(
            client_id=client_id, response_type=response_type,
            response_mode=response_mode, redirect_url=redirect_url,
            state=state
        )
        ParameterCache.set_value(key=key, value=temporal_value)
        redirect_to = f"/oauth2/login_page?key={key}"
        return redirect(redirect_to)

    # 사용자 email 값을 이용하여 device-token을 확인
    email = request.session['email']
    web3c = Web3Client()
    n_contract = NotificationContract(web3c)
    device_token = n_contract.get_device_token(email)

    # client-id를 이용하여 서비스 정보를 확인
    cm_contract = ClientManagementContract(web3c)
    summary: ClientSummary = cm_contract.get_client_summary(client_id)

    # 사용자에게 메시지를 전송하고 이에 대한 권한 승인 응답을 받아야 한다.
    message_cover = FcmCover(title='', body='')
    temporary_id = random_string()
    data = {
        'type': 'authentication_code',
        'unlock_code': temporary_id,
        'client_id': summary.client_id,
        # 'client_name': summary.name
    }
    req_message = FcmMessage(device_token, message_cover, data)
    send_fcm_notification(req_message)
    Locker.register(temporary_id)

    # 사용자 승락/거절 응답을 대기
    count = 0
    while count != 20:
        time.sleep(1)
        count += 1
        auth_code = Locker.storage[temporary_id]
        if auth_code is not None:
            break
    if auth_code is False or count == 20:
        del request.session['email']
        return HttpResponse('access denied')

    # 제공한 auth_code는 1회를 초과하여 사용되어서는 안된다.
    context = {
        'auth_code': auth_code['code'],
        'state': auth_code['state']
    }

    # context를 email과 mapping하여 저장한다. 이는 추후에 client가 접속할 때 알맞은 email로 연결하기 위함이다.
    AuthCodeCache.set_value(auth_code['code'], email)

    redirect_to = f"{redirect_url}?state={state}&code={auth_code}"
    return redirect(redirect_to)


def fcm_authorize(request):
    try:
        # reply는 auth_code를 의미한다. =>
        reply = request.GET['reply']
        unlock_code = request.GET['unlock_code']
        auth_code = request.GET['code']
        state = request.GET['request']
        value = {
            'auth_code': auth_code,
            'state': state
        }
    except Exception:
        print("FCM Authorize parameter unfulfilled.")
        pass

    Locker.storage[unlock_code] = value
    print("Auth_code Request is accepted by User")

    """reply 는 auth_code를 의미한다. => auth_code 와 state를 쓰기로 함."""
