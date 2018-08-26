===================
JasperReports Tools
===================


.. image:: https://img.shields.io/pypi/v/jr_tools.svg
        :target: https://pypi.python.org/pypi/jr_tools

.. image:: https://img.shields.io/travis/erickgnavar/jasper-reports-tools.svg
        :target: https://travis-ci.org/erickgnavar/jasper-reports-tools

.. image:: https://readthedocs.org/projects/jasperreports-tools/badge/?version=latest
        :target: https://jasperreports-tools.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. image:: https://pyup.io/repos/github/erickgnavar/jr_tools/shield.svg
     :target: https://pyup.io/repos/github/erickgnavar/jr_tools/
     :alt: Updates


A collection of tools to handle Jasper Reports with python


* Free software: MIT license
* Documentation: http://jasperreports-tools.readthedocs.io.

Tested with JasperServer CE 6.4


Features
--------

* Client to get reports in API available formats(PDF, xls, etc)
* CLI: run ``jr_tools --help`` to get the list of available commands
* CLI: load resources from yaml file ``jr_tools load path_to_yaml_file``

Development
-----------

For development there is a docker-compose based configuration to start jasper server and mysql.

Use the below commands to handle the docker setup:

* ``make docker_up``: this will launch docker-compose services, it's going to take a few minutes to download the required images and setup everything.
* ``make docker_down``: this will shutdown the launched containers.
* ``make mysql_shell``: this will launch a mysql console to interact with the database, by default it connects to ``demo`` database.
* ``make mysql_shell_root``: the same as above but use the ``root`` user.

Credentials:

Jasper Server:

* username: ``jasperadmin``
* password: ``jasperadmin``

MySQL:

* username: ``demo``
* password: ``demo``
* root password: ``root``
* default database: ``demo``

After the setup is complete you can enter to http://localhost:8080 and login using the credentials from above.

TODO
----
* Django helper to consume reports and converto to Django responses


Credits
---------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
