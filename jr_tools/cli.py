# -*- coding: utf-8 -*-

"""Console script for jr_tools."""
from __future__ import absolute_import

import click
import yaml

from jr_tools.client import ALLOWED_REPORT_FORMATS, Client


@click.group()
def main():
    """
    Console scripts to interact with Jasper Server
    """


@click.argument('output', type=click.Path())
@click.argument('report_path', type=click.STRING)
@click.option('--format', default='pdf', help='Report format {}'.format(', '.join(ALLOWED_REPORT_FORMATS)))
@click.option('--params-quantity', type=click.INT, default=0)
@main.command()
def run_report(report_path, output, params_quantity, format):
    """
    Run report in Jasper Server and save the result to file

    The credenciales will be read from environment variables:

    For example:

    JASPER_URL: http://localhost:8080/jasperserver

    JASPER_USERNAME: jasperadmin

    JASPER_PASSWORD: secret
    """
    params = {}
    if params_quantity:
        for _ in range(params_quantity):
            name = input('Parameter name: ')
            value = input('Parameter value: ')
            params[name] = value

    client = Client()
    result = client.run_report(report_path, params, format)
    if result is not None:
        with open(output, 'wb') as f:
            f.write(result)
        click.echo('Report was saved: {}'.format(output))
    else:
        click.echo('Report not found')


@click.argument('config', type=click.Path())
@main.command(help='Load resources to jasper server')
def load(config):
    with open(config) as f:
        data = yaml.load(f.read())
        client = Client()

        click.echo('Deleting previous reports...')
        for value in data.get('reports', []):
            client.delete_report(value['uri'])

        click.echo('Uploading files...')
        for value in data.get('files', []):
            client.upload_file(value)

        click.echo('Uploading reports...')
        for value in data.get('reports', []):
            client.upload_report(value)
