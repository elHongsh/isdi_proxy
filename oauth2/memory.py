class AuthProcessParameter:
    def __init__(self, client_id: str, response_type: str, redirect_url: str, response_mode: str, state: str):
        self.client_id = client_id
        self.response_type = response_type
        self.redirect_url = redirect_url
        self.response_mode = response_mode
        self.state = state


class ParameterCache:
    """로그인 과정에서 파라미터들을 key 로 변경해야 할 때 ParameterCache 가 임시로 보관한다."""
    parameter_map = dict()

    @staticmethod
    def set_value(key: str, value: AuthProcessParameter):
        ParameterCache.parameter_map[key] = value

    @staticmethod
    def get_value(key: str) -> AuthProcessParameter:
        return ParameterCache.parameter_map[key]


class AuthCodeCache:
    """code 와 email 간의 연관성을 제공하여 device-token 을 찾을 때 사용한다."""
    code_email_map = dict()

    @staticmethod
    def set_value(key: str, value: str):
        AuthCodeCache.code_email_map[key] = value

    @staticmethod
    def get_value(key: str) -> str:
        return AuthCodeCache.code_email_map[key]
