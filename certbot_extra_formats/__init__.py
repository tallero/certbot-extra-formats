#!/usr/bin/env python3

#    certbot_extra_formats
#
#    ----------------------------------------------------------------------
#    Copyright © 2018, 2019, 2020, 2021, 2022, 2023  Pellegrino Prevete
#
#    All rights reserved
#    ----------------------------------------------------------------------
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.
#


from subprocess import check_output as sh
from os import listdir as ls
from os.path import join as pjoin
from argparse import ArgumentParser
from os import walk

name = 'certbot_extra_formats'
version = "0.1.4"

def write_cert(
        app, 
        certroot="/etc/letsencrypt/live/",
        verbose=False):
    """Combine and write let's encrypt certificates
       compatible with given application.

    Args:
        app (str): application that requests the certificate;
        certroot (str): where the Let's Encrypt certificates 
                        are (default: /etc/letsencrypt/live/);
        verbose (bool): extended output 
    Returns:
        True if the certificate has been written to certroot
        dir with 'app.pem' name, False otherwise.

    """
    out = {}
    if verbose: 
        print(app + ":")

    # Check certroot and obtain domains
    try:
        certroot = certroot if certroot.endswith("/") else certroot + "/"
        domains = []
        for (dirpath,
             dirnames,
             filenames) in walk(certroot):
            domains.extend(dirnames)
            break
    except FileNotFoundError as e:
        print(" ".join("ERROR: certbot not configured or",
                       "present:\n\t",
                       certroot,
                       "not found or empty"))
        domains = []

    for domain in domains:
        path = pjoin(certroot, domain)
        certname = pjoin(path, app + '.pem')
        certs = {pem:pjoin(path, pem) for pem in ls(path)}

        # Certificate generation depending on application
        apps = {"ejabberd":[
                  'cat', ' ', certs['privkey.pem'],
                         ' ', certs['fullchain.pem'], ' > ',
                    certname],
                "haproxy":[
                  'cat', ' ', certs['privkey.pem'],
                         ' ', certs['fullchain.pem'], ' > ',
                    certname],
                "lighttpd":[
                   'cat', ' ', certs['cert.pem'],
                          ' ', certs['privkey.pem'], ' > ',
                     certname],
                "tomcat7":[
                  "echo 'IMPORTANT: the common name has to be your FQDN, for instance : www.myexample.com'", '&&'
                  'keytool -genkey -alias tomcat -keyalg RSA -keystore /usr/share/tomcat/.keystore -keysize 2048', '&&',
                  'keytool -certreq -alias tomcat -file request.csr -keystore /usr/share/tomcat/.keystore', '&&',
                  'systemctl stop tomcat', '&&',
                  'iptables -F -t nat', '&&',
                  'certbot certonly --csr request.csr', '&&',
                  'keytool -import -trustcacerts -alias tomcat -file 0000_chain.pem -keystore /usr/share/tomcat7/.keystore', '&&',
                  'echo', """modify tomcat server.xml (i.e. /etc/tomcat7/server.xml) to make 8443 port connector to look like:
<Connector port="8443" protocol="HTTP/1.1" SSLEnabled="true"
maxThreads="150" scheme="https" secure="true"
clientAuth="false" sslProtocol="TLS" KeystoreFile="/usr/share/tomcat7/.keystore" KeystorePass="Password_you_have_set_at_key_creation" />""", '&&',
                  'systemctl restart tomcat', '&&',
                  "echo 'restore your firewall'"],
                "httpd-dh":[
                  'cat', ' ', certs['cert.pem'],
                         ' ', '/etc/pki/tls/certs/dh2048.pem', ' > ',
                              '/etc/pki/tls/certs/http-' + domain + '.crt']}

        # Create certificate
        if apps.get(app, False):
            command = "".join(apps[app])
            out[domain] = sh([command], shell=True)
        else:
            print("ERROR: uknown application: " + app)
            return False 
        if out[domain] == b'':
            if verbose:
                print("\twriting " + domain)


    if all(out[k] == b'' for k in out.keys()):
            return True

def main():
    parser = ArgumentParser(
               description=("Writes a \"Let's Encrypt\" certificate "
                            "compatible with a given application"))
    parser.add_argument(
      '--verbose', 
      dest='verbose',
      action='store_true',
      default=False,
      help="extended output")
    parser.add_argument(
      'app',
      nargs='*',
      action='store',
      default=['lighttpd'],
      help=("application that request the certificate: "
            "ejabberd, haproxy, lighttpd, tomcat7, "
            "httpd-dh (apache <= 2.4.7 with DH parameters)"))
    parser.add_argument(
      '--certroot',
      dest='certroot',
      action='store',
      default="/etc/letsencrypt/live/",
      help="directory which contains the letsencrypt certificates")
    args = parser.parse_args()

    for app in args.app:
        written = write_cert(
                    app,
                    certroot=args.certroot,
                    verbose=args.verbose)

if __name__ == "__main__":
    main()

# vim:set sw=2 sts=-1 et:
