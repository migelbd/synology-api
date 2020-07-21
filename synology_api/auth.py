import requests
import logging

from synology_api.exceptions import SynologyApiError

logger = logging.getLogger(__name__)

def raise_exception(code, response_data):
    from synology_api import exceptions
    exceptions_map = {
        100: exceptions.UnknownError,
        101: exceptions.InvalidParameter,
        102: exceptions.InvalidRequestAPI,
        103: exceptions.MethodNotExists,
        104: exceptions.NotSupportVersion,
        105: exceptions.ForbiddenRequest,
        106: exceptions.SessionTimeout,
        107: exceptions.SessionInterrupted,
        400: exceptions.NoSuchAccountOrIncorrectPassword,
        401: exceptions.AccountDisabled,
        402: exceptions.PermissionDenied,
        403: exceptions.VerificationCode2StepRequired,
        404: exceptions.FailedAuthenticate2StepVerificationCode,

    }
    exc = exceptions_map.get(code, exceptions.UnknownError)
    raise exc(response_data=response_data)


class Authentication:
    def __init__(self, ip_address, port, username, password, secure=False, **kwargs):
        self._ip_address = ip_address
        self._port = port
        self._username = username
        self._password = password
        self._sid = None
        self._session_expire = True
        schema = 'https' if secure else 'http'
        self._base_url = '%s://%s:%s/webapi/' % (schema, self._ip_address, self._port)
        self.is_raise_exception = kwargs.get('raise_exceptions', True)
        self.full_api_list = {}
        self.app_api_list = {}

    def get_data_or_error(self, response) -> dict:
        response_data = response.json()
        if self.is_raise_exception and 'error' in response_data:
            raise_exception(response_data['error']['code'], response_data)
        return response_data

    def login(self, application):
        login_api = 'auth.cgi?api=SYNO.API.Auth'
        param = {'version': '2', 'method': 'login', 'account': self._username,
                 'passwd': self._password, 'session': application, 'format': 'cookie'}

        if not self._session_expire:
            if self._sid is not None:
                self._session_expire = False
                return 'User already logged'
        else:
            session_request = requests.get(self._base_url + login_api, param)
            response_data: dict = self.get_data_or_error(session_request)

            self._sid = response_data['data']['sid']
            self._session_expire = False
            logger.info('User logging... New session started!')
            return 'User logging... New session started!'

    def logout(self, application):
        logout_api = 'auth.cgi?api=SYNO.API.Auth'
        param = {'version': '2', 'method': 'logout', 'session': application}

        response = requests.get(self._base_url + logout_api, param)
        if response.json()['success'] is True:
            self._session_expire = True
            self._sid = None
            return 'Logged out'
        else:
            self._session_expire = True
            self._sid = None
            return 'No valid session is open'

    def get_api_list(self, app=None):
        query_path = 'query.cgi?api=SYNO.API.Info'
        list_query = {'version': '1', 'method': 'query', 'query': 'all'}

        response = requests.get(self._base_url + query_path, list_query).json()

        if app is not None:
            for key in response['data']:
                if app.lower() in key.lower():
                    self.app_api_list[key] = response['data'][key]
        else:
            self.full_api_list = response['data']

        return

    def show_api_name_list(self):
        prev_key = ''
        for key in self.full_api_list:
            if key != prev_key:
                print(key)
                prev_key = key
        return

    def show_json_response_type(self):
        for key in self.full_api_list:
            for sub_key in self.full_api_list[key]:
                if sub_key == 'requestFormat':
                    if self.full_api_list[key]['requestFormat'] == 'JSON':
                        print(key + '   Returns JSON data')
        return

    def search_by_app(self, app):
        print_check = 0
        for key in self.full_api_list:
            if app.lower() in key.lower():
                print(key)
                print_check += 1
                continue
        if print_check == 0:
            print('Not Found')
        return

    def request_data(self, api_name, api_path, req_param, method=None, response_json=True):  # 'post' or 'get'

        # Convert all booleen in string in lowercase because Synology API is waiting for "true" or "false"
        for k, v in req_param.items():
            if isinstance(v, bool):
                req_param[k] = str(v).lower()

        if method is None:
            method = 'get'

        req_param['_sid'] = self._sid
        response = None
        if method == 'get':
            url = ('%s%s' % (self._base_url, api_path)) + '?api=' + api_name
            response = requests.get(url, req_param)
        elif method == 'post':
            url = ('%s%s' % (self._base_url, api_path)) + '?api=' + api_name
            response = requests.post(url, req_param)

        if response and response.status_code != 200:
            raise SynologyApiError(response.text)

        if response_json is True:
            return self.get_data_or_error(response)
        else:
            return response

    @property
    def sid(self):
        return self._sid

    @property
    def base_url(self):
        return self._base_url
