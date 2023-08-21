# certbot-extra-formats

[![Python 3.x Support](https://img.shields.io/pypi/pyversions/Django.svg)](https://python.org)
[![License: AGPL v3+](https://img.shields.io/badge/license-AGPL%20v3%2B-blue.svg)](http://www.gnu.org/licenses/agpl-3.0)

Writes a \"Let's Ecrypt\" certificate
compatible with a given application

## Installation

*certbot-extra-formats* is available through the
[Python Package Index (PyPI)](https://pypi.org/).
Pip is already installed if you are using Python
3 >=3.4 downloaded from [python.org](https://python.org);
if you're using a GNU/Linux distribution,
you can find how to install it on
this [page](https://packaging.python.org/guides/installing-using-linux-tools/#installing-pip-setuptools-wheel-with-linux-package-managers).
After setting up pip, you can install *certbot-extra-formats* by simply typing in your terminal

    pip3 install certbot-extra-formats

## Usage

    $ certbot-extra-formats --help

    usage: certbot-extra-formats [-h] [--verbose] [--certroot CERTROOT] [app ...]
    
    Writes a "Let's Encrypt" certificate compatible with a given application
    
    positional arguments:
      app                  application that request the certificate: ejabberd, haproxy, lighttpd,
                           tomcat7, httpd-dh (apache <= 2.4.7 with DH parameters)
    
    options:
      -h, --help           show this help message and exit
      --verbose            extended output
      --certroot CERTROOT  directory which contains the letsencrypt certificates

## About

This program is licensed under
[GNU Affero General Public License v3 or later](https://www.gnu.org/licenses/agpl-3.0.en.html)
by [Pellegrino Prevete](http://prevete.ml).
If you find this program useful, consider offering me a
[beer](https://patreon.com/tallero), a new
[computer](https://patreon.com/tallero)
or a part time remote
[job](mailto:pellegrinoprevete@gmail.com)
to help me pay the bills.
