import json
import os
from typing import Dict

import requests

SERVER_KEY = os.environ.get('SERVER_KEY')
PROJECT_ID = os.environ.get('PROJECT_ID')
REGISTRATION_TOKEN = os.environ.get('REGISTRATION_TOKEN')
GOOGLE_URL = os.environ.get('GOOGLE_URL')


class FcmCover:
    """Notification 부분을 표현하는 클래스"""

    def __init__(self, title: str, body: str):
        self.title = title
        self.body = body


class FcmMessage:
    """FCM Push Message 전송 시 필요한 데이터 클래스"""

    def __init__(self, receiver, cover: FcmCover, data: Dict[str, str]):
        self.receiver = receiver
        self.cover = cover
        self.data = data


def send_fcm_notification(message: FcmMessage, control=False):
    """FCM 푸시 메시지 요청 주소"""
    # 인증 정보(서버 키)를 헤더에 담아 FCM 메시지 서버에게 전달
    headers = {
        'Authorization': 'key=' + SERVER_KEY,
        'Content-Type': 'application/json; UTF-8'
    }

    # 보낼 내용과 대상을 지정
    content = dict()
    if type(message.receiver) is list:  # 복수 대상
        content['registration_ids'] = message.receiver
    else:  # 단일 대상
        content['to'] = message.receiver
    content['data'] = message.data

    # SAMPLE
    # content = {
    #     'registration_ids': ids,
    #     'notification': {
    #         'title': title,
    #         'body': body
    #     }
    #     'data': {
    #     }
    # }

    # json 파싱 후 requests 모듈로 FCM 서버에 요청
    return requests.post(GOOGLE_URL, data=json.dumps(content), headers=headers).text
