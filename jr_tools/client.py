import base64
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

    @property
    def resources_url(self):
        return '{}/rest_v2/resources'.format(self.url)

    @property
    def reports_url(self):
        return '{}/rest_v2/reports'.format(self.url)

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

    def _delete(self, url):
        return requests.delete(url, headers={
            'accept': 'application/json',
        }, auth=(self.username, self.password))

    def _get(self, url, params=None):
        return requests.get(url, headers={
            'accept': 'application/json',
        }, auth=(self.username, self.password), params=params)

    def _post(self, url, data=None, json=None, headers=None):
        if headers is None:
            headers = {}
        headers.update({
            'Accept': 'application/json',
        })
        return requests.post(
            url,
            data=data,
            json=json,
            headers=headers,
            auth=(self.username, self.password),
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

    def upload_file(self, data):
        assert data['uri'].startswith('/'), 'The uri must start with /'
        label = data['uri'].split('/')[-1]
        path = data['uri'].split('/')[0:-1]
        path = '/'.join(path)
        headers = {
            'content-type': 'application/repository.file+json',
        }
        url = '{base}{path}'.format(
            base=self.resources_url,
            path=data['uri'],
        )
        self._delete(url)
        with open(os.path.abspath(data['path']), 'rb') as f:
            content = f.read()
        content = base64.encodestring(content)
        url = '{base}{path}'.format(
            base=self.resources_url,
            path=path,
        )
        data = {
            'type': data['type'],
            'content': content.decode(),
            'label': label,
        }
        self._post(url, headers=headers, json=data)

    def delete_report(self, uri):
        assert uri.startswith('/'), 'The uri must start with /'
        url = '{base}{path}'.format(
            base=self.resources_url,
            path=uri,
        )
        self._delete(url)

    def upload_report(self, data):
        assert data['uri'].startswith('/'), 'The uri must start with /'
        label = data['uri'].split('/')[-1]
        path = data['uri'].split('/')[0:-1]
        path = '/'.join(path)
        prefix = data['uri'][1:].replace('/', '_')
        inputs = []
        for param in data['params']:
            inputs.append({
                'inputControlReference': {
                    'uri': self.create_input_control(param, prefix)
                }
            })
        post_data = {
            'label': label,
            'jrxml': {
                'jrxmlFileReference': {
                    'uri': data['jrxml_uri']
                }
            },
            'dataSource': {
                'dataSourceReference': {
                    'uri': data['data_source_uri']
                }
            },
            'inputControls': inputs
        }
        url = '{base}{path}'.format(
            base=self.resources_url,
            path=path,
        )
        headers = {
            'content-type': 'application/repository.reportUnit+json',
        }
        self._post(url, headers=headers, json=post_data)

    def create_input_control(self, data, prefix):
        self.delete_previous_control_input(data, prefix)
        headers = {
            'content-type': 'application/repository.dataType+json'
        }
        data_type_url = '{}/DataTypes/{}'.format(
            self.resources_url,
            prefix,
        )
        res = self._post(data_type_url, json={
            'type': data['type'],
            'label': data['label']
        }, headers=headers)
        data_type_uri = res.json()['uri']
        headers = {
            'content-type': 'application/repository.inputControl+json',
        }
        input_control_url = '{}/InputControls/{}'.format(
            self.resources_url,
            prefix,
        )
        res = self._post(input_control_url, json={
            'type': 2,  # single value
            'label': data['label'],
            'mandatory': data.get('mandatory', False),
            'visible': data.get('visible', True),
            'dataType': {
                'dataTypeReference': {
                    'uri': data_type_uri
                }
            }
        }, headers=headers)
        return res.json()['uri']

    def delete_previous_control_input(self, data, prefix):
        input_control_url = '{}/InputControls/{}/{}'.format(
            self.resources_url,
            prefix,
            data['label'],
        )
        self._delete(input_control_url)

        data_type_url = '{}/DataTypes/{}/{}'.format(
            self.resources_url,
            prefix,
            data['label'],
        )
        self._delete(data_type_url)
