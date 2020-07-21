class SynologyApiError(Exception):
    code = 0
    message = 'SynologyApiError'
    response_data = None

    def __init__(self, message=None, response_data=None, *args):
        self.response_data = response_data
        super().__init__(message or self.message, *args)


class FailRequest(SynologyApiError):
    message = 'Request not success'


class UnknownError(SynologyApiError):
    code = 100
    message = 'Unknown error'


class InvalidParameter(SynologyApiError):
    code = 101
    message = 'Invalid parameter'


class InvalidRequestAPI(SynologyApiError):
    code = 102
    message = 'The requested API does not exist'


class MethodNotExists(SynologyApiError):
    code = 103
    message = 'The requested method does not exist'


class NotSupportVersion(SynologyApiError):
    code = 104
    message = 'The requested version does not support the functionality'


class ForbiddenRequest(SynologyApiError):
    code = 105
    message = 'The logged in session does not have permission'


class SessionTimeout(SynologyApiError):
    code = 106
    message = 'Session timeout'


class SessionInterrupted(SynologyApiError):
    code = 107
    message = 'Session interrupted by duplicate login'


class NoSuchAccountOrIncorrectPassword(SynologyApiError):
    code = 400
    message = 'No such account or incorrect password'


class AccountDisabled(SynologyApiError):
    code = 401
    message = 'Account disabled'


class PermissionDenied(SynologyApiError):
    code = 402
    message = 'Permission denied'


class VerificationCode2StepRequired(SynologyApiError):
    code = 403
    message = '2-step verification code required'


class FailedAuthenticate2StepVerificationCode(SynologyApiError):
    code = 404
    message = 'Failed to authenticate 2-step verification code'
