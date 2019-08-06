class Locker:
    """FCM 에 대한 요청 결과로 온 사용자 응답에 대한 값을 저장하는 클래스"""
    storage = dict()

    @staticmethod
    def check(key: str):
        value = Locker.storage[key]
        return value

    @staticmethod
    def register(key: str):
        Locker.storage[key] = None
