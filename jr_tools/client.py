import logging
import os

import requests

from . import exceptions


ALLOWED_REPORT_FORMATS = (
    'pdf', 'html', 'xls', 'xlsx', 'rtf',
    'csv', 'xml', 'docx', 'odt', 'ods', 'jrprint',
)


logger = logging.getLogger(__name__)


class Client(object):
    """
    Client allows to retrieve reports from JasperServer using rest API V2
    """
    _template = '{url}{api_base}{path}.{output_format}'
    _reports_endpoint = '/rest_v2/reports'

    def __init__(self, *args, **kwargs):
        self.url = kwargs.get('url', os.environ.get('JASPER_URL'))
        self.username = kwargs.get('username', os.environ.get('JASPER_USERNAME'))
        self.password = kwargs.get('password', os.environ.get('JASPER_PASSWORD'))
        self._check_connection_params()

    def _check_connection_params(self):
        if not all([self.url, self.username, self.password]):
            raise ValueError('The connection values are not complete')

    def _check_output_format(self, output_format):
        if output_format.lower() not in ALLOWED_REPORT_FORMATS:
            raise exceptions.InvalidOutputFormat(
                'The output format must be one of the following: {}'.format(', '.join(ALLOWED_REPORT_FORMATS))
            )

    def _prepare_url(self, report_path, output_format):
        """
        Make the full path url of the report in JasperServer API
        """
        return self._template.format(
            url=self.url,
            api_base=self._reports_endpoint,
            path=report_path,
            output_format=output_format.lower(),
        )

    def run_report(self, path, params, output_format='pdf'):
        """
        Returns binary content of the report requested or None
        if the report path does not exists in jasper server
        """
        url = self._prepare_url(path, output_format)
        self._check_output_format(output_format)
        try:
            auth = (self.username, self.password)
            response = requests.get(url, params=params, auth=auth)
            if response.status_code == 200:
                return response.content
            else:
                return None
        except (requests.ConnectionError, requests.ConnectTimeout) as ex:
            logger.error(str(ex))
            raise exceptions.ConnectionError
