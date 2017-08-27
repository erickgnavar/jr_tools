=====
Usage
=====

From python code
----------------

Run a report and get the binary result

.. code-block:: python

    from jr_tools.client import Client

    client = Client(url='http://localhost:8080/jasperserver', username='jasperadmin', password='secret')
    result = client.run_report('/path/to/report', {'id': 1}, 'pdf')

From command line
-----------------

Get all available commands

.. code-block:: console

    $ jr_tools --help


Run and save a report

.. code-block:: console

    $ jr_tools run_report /path/to/report result_file.pdf --format pdf

To get more info about the optional arguments run:

.. code-block:: console

    $ jr_tools run_report --help
