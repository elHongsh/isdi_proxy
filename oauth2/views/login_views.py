import time

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from eth3.contracts.client_management_deployment import ClientManagementContract, ClientSummary
from eth3.contracts.notification_deployment import NotificationContract
from eth3.web3_client import Web3Client
from fcm import notification
from fcm.notification import FcmCover, FcmMessage
from oauth2.locker import Locker
from oauth2.memory import AuthProcessParameter, ParameterCache
from oauth2.secret_generator import random_string


def logout(request):
    if 'email' in request.session:
        del request.session['email']
        msg = 'successfully logged out.'
    else:
        msg = 'already logged out.'
    return HttpResponse(msg)


def login_page(request):
    return render(request, template_name='login_page.html')


@method_decorator(csrf_exempt, name='dispatch')
def login(request):
    try:
        key = request.POST['key']
        email = request.POST['email']
        password = request.POST['password']
    except KeyError:
        return HttpResponse(status=400, content='login process unfinished')

    # authorize 에서 key 로 저장했던 데이터를 다시 획득
    recovered_oauth_parameter = ParameterCache.get_value(key)
    client_id = recovered_oauth_parameter.client_id
    response_type = recovered_oauth_parameter.response_type
    response_mode = recovered_oauth_parameter.response_mode
    redirect_url = recovered_oauth_parameter.redirect_url
    state = recovered_oauth_parameter.state

    # email 을 사용하여 로그인 한 사용자의 device-token 을 획득
    web3c = Web3Client()
    n_contract = NotificationContract(web3c)
    token = n_contract.get_device_token(email)

    # client-id 를 이용하여 사용자가 로그인 하려는 사이트 정보를 획득'
    cm_contract = ClientManagementContract(web3c)
    summary: ClientSummary = cm_contract.get_client_summary(client_id)

    # 로그인 요청을 위한 FCM 데이터를 생성(title, body 는 사용되지 않는다)
    message_cover = FcmCover(title='', body='')
    unlock_code = random_string()
    data = {
        'type': 'login',
        'unlock_code': unlock_code,
        'client_id': summary.client_id,
        'password': password,
        # 'client_name': summary.name,
    }
    login_req_message = FcmMessage(token, message_cover, data)
    notification.send_fcm_notification(login_req_message)

    # 로그인 요청에 대한 사용자 응답 대기
    Locker.register(unlock_code)
    lock_value = None
    count = 0
    while count != 20:
        time.sleep(1)
        count += 1
        lock_value = Locker.storage[unlock_code]
        if lock_value is not None:
            break
    if lock_value is False or count == 20 or lock_value is None:
        return HttpResponse('login denied')

    # email, client-PubKey 를 session 에 등록하고 authorize 프로세스로 이동
    request.session['email'] = email
    request.session['password'] = password

    redirect_to = f"/oauth2/authorize?client_id={client_id}&response_type={response_type}" \
        f"&response_mode={response_mode}&redirect_url={redirect_url}&state={state}"
    return redirect(redirect_to)


def fcm_login_response(request):
    try:
        reply = request.GET['reply']
        unlock_code = request.GET['unlock_code']
    except KeyError:
        print('Not enough paramters to enter the fcm_login_response process.')

    if reply == 'true':
        Locker.storage[unlock_code] = True
        print(f'User enter the unlock_code({unlock_code})')
    else:
        print(f'User denied to unlock the code.')
