from .base import BaseApi


class DownloadStation(BaseApi):

    def __init__(self, ip_address, port, username, password, secure=False, raise_exceptions=True):
        super().__init__(ip_address, port, username, password, secure, raise_exceptions)
        self._bt_search_id = ''
        self._bt_search_id_list = []

    def get_info(self):
        return self.request('Info', 'getinfo')

    def get_config(self):
        return self.request('Info', 'getconfig')

    def set_server_config(self, bt_max_download=None, bt_max_upload=None, emule_max_download=None,
                          emule_max_upload=None, nzb_max_download=None, http_max_download=None, ftp_max_download=None,
                          emule_enabled=None, unzip_service_enabled=None, default_destination=None,
                          emule_default_destination=None):

        params = dict()
        for key, val in locals().items():
            if key not in ['self', 'api_name', 'info', 'api_path', 'req_param']:
                if val is not None:
                    params[str(key)] = val
        return self.request('Info', 'setserverconfig', params)

    def schedule_info(self):
        return self.request('Schedule', 'getconfig')

    def schedule_set_config(self, enabled: bool = False, emule_enabled: bool = False):
        req_param = {'enabled': str(enabled).lower(), 'emule_enabled': str(emule_enabled).lower()}
        return self.request('Schedule', 'setconfig', req_param)

    def tasks_list(self, additional_param=None, offset=0, limit=-1):
        if additional_param is None:
            additional_param = ['detail', 'transfer', 'file', 'tracker', 'peer']
        req_param = {'additional': additional_param, 'limit': limit, 'offset': offset}

        if isinstance(additional_param, (list, tuple,)):
            req_param['additional'] = ",".join(additional_param)

        return self.request('Task', 'list', req_param)

    def tasks_info(self, task_id, additional_param=None):
        if additional_param is None:
            additional_param = ['detail', 'transfer', 'file', 'tracker', 'peer']
        req_param = {'id': task_id, 'additional': additional_param}

        if isinstance(additional_param, (list, tuple,)):
            req_param['additional'] = ",".join(additional_param)

        if isinstance(task_id, (list, tuple,)):
            req_param['id'] = ",".join(task_id)

        return self.request('Task', 'getinfo', req_param)

    def delete_task(self, task_id, force: bool = False):
        req_param = {'id': task_id, 'force_complete': str(force).lower()}

        if isinstance(task_id, (list, tuple,)):
            req_param['id'] = ",".join(task_id)

        return self.request('Task', 'delete', req_param)

    def pause_task(self, task_id):
        req_param = {'id': task_id}

        if isinstance(task_id, (list, tuple,)):
            req_param['id'] = ",".join(task_id)

        return self.request('Task', 'pause', req_param)

    def resume_task(self, task_id):
        req_param = {'id': task_id}

        if isinstance(task_id, (list, tuple,)):
            req_param['id'] = ",".join(task_id)

        return self.request('Task', 'resume', req_param)

    def create_task(self, uri, destination=None, unzip_password=None):
        """
        Create task
        :param uri: Accepts HTTP/FTP/magnet/ED2K links or the file path starting with a shared folder, separated by ","
        :param destination: Download destination path starting with a shared folder
        :param unzip_password:  Password for unzipping download tasks
        :return:
        """
        params = dict(uri=uri)
        if isinstance(uri, (list, tuple,)):
            params['uri'] = ','.join(uri)
        if destination:
            params['destination'] = destination
        if unzip_password:
            params['unzip_password'] = unzip_password

        return self.request('Task', 'create', params)

    def edit_task(self, task_id, destination='sharedfolder'):
        req_param = {'id': task_id, 'destination': destination}

        if isinstance(task_id, (list, tuple,)):
            req_param['id'] = ",".join(task_id)

        return self.request('Task', 'edit', req_param)

    def get_statistic_info(self):
        return self.request('Statistic', 'getinfo')

    def get_rss_info_list(self, offset=None, limit=None):
        param = dict()
        if offset is not None:
            param['offset'] = offset
        if limit is not None:
            param['limit'] = limit

        return self.request('RSS.Site', 'list', param)

    def refresh_rss_site(self, rss_id):
        param = {'id': rss_id}

        if isinstance(rss_id, (list, tuple,)):
            param['id'] = ','.join(rss_id)

        return self.request('RSS.Site', 'refresh', param)

    def rss_feed_list(self, rss_id, offset=None, limit=None):
        param = {'id': rss_id}

        if isinstance(rss_id, (list, tuple,)):
            param['id'] = ','.join(rss_id)

        if offset is not None:
            param['offset'] = offset
        if limit is not None:
            param['limit'] = limit

        return self.request('RSS.Feed', 'list', param)

    def start_bt_search(self, keyword, module='all') -> str:
        response = self.request('BTSearch', 'start', dict(
            keyword=keyword,
            module=module
        ))
        self._bt_search_id = response['data']['taskid']

        self._bt_search_id_list.append(self._bt_search_id)

        return self._bt_search_id

    def get_bt_search_results(self, taskid, offset=None, limit=None, sort_by=None, sort_direction=None,
                              filter_category=None, filter_title=None):

        param = {'taskid': taskid}

        for key, val in locals().items():
            if key not in ['self', 'api_name', 'info', 'api_path', 'param', 'taskid']:
                if val is not None:
                    param[str(key)] = val

        if isinstance(taskid, (list, tuple,)):
            param['id'] = ','.join(taskid)

        return self.request('BTSearch', 'list', param)

    def get_bt_search_category(self):
        return self.request('BTSearch', 'get')

    def clean_bt_search(self, task_id):
        param = {'taskid': task_id}

        if isinstance(task_id, (list, tuple,)):
            param['taskid'] = ','.join(task_id)
            for item in param['taskid']:
                self._bt_search_id_list.remove(item)
        else:
            self._bt_search_id_list.remove(task_id)

        return self.request('BTSearch', 'clean', param)

    def get_bt_module(self):
        return self.request('BTSearch', 'getModule')
