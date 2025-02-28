

from mantis import const


class RESTController:
    def __init__(self, base_url, auth, timeout):
        self._base_url = base_url

        self.auth = auth
        self.timeout = timeout

        self.http_header = self.get_http_header()

    def get_http_header(self):
        headers = {
            'Content-Type': const.REST.CONTENT_TYPE_JSON
        }
        if self.auth:
            headers['Authorization'] = self.auth

        return headers

# class ProjectsHandler:
#    def

# class ProjectsHandler:
#    def
