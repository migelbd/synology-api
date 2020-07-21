from . import auth as syn


class BaseApi:
    __API_PREFIX = 'SYNO'

    def __init__(self, ip_address, port, username, password, secure=False, raise_exceptions=True):
        self.session = syn.Authentication(ip_address, port, username, password, secure,
                                          raise_exceptions=raise_exceptions)

        self.session.login(self.__api_name)
        self.session.get_api_list(self.__api_name)
        self.request_data = self.session.request_data
        self.app_api_list = self.session.app_api_list

        self._sid = self.session.sid
        self.base_url = self.session.base_url

    @property
    def __api_name(self):
        return type(self).__name__

    def logout(self):
        self.session.logout(self.__api_name)

    def request(self, api_name, method, params=None):
        if not str(api_name).startswith(self.__API_PREFIX):
            api_name = f'{self.__API_PREFIX}.{self.__api_name}.{api_name}'
        info = self.app_api_list[api_name]
        api_path = info['path']
        req_param = {'version': info['maxVersion'], 'method': method}
        if params:
            req_param.update(params)
        return self.request_data(api_name, api_path, req_param)
