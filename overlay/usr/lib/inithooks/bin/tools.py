#!/usr/bin/python
"""Set tools password

Option:
    --pass=     unless provided, will ask interactively

"""

import sys
import getopt

from dialog_wrapper import Dialog
from executil import system

def usage(s=None):
    if s:
        print >> sys.stderr, "Error:", s
    print >> sys.stderr, "Syntax: %s [options]" % sys.argv[0]
    print >> sys.stderr, __doc__
    sys.exit(1)

def main():
    try:
        opts, args = getopt.gnu_getopt(sys.argv[1:], "h", ['help', 'pass='])
    except getopt.GetoptError, e:
        usage(e)

    password = ""
    username = "admin"

    for opt, val in opts:
        if opt in ('-h', '--help'):
            usage()
        elif opt == '--pass':
            password = val

    if not password:
        d = Dialog('TurnKey Linux - First boot configuration')
        password = d.get_password("Tools page admin Password", "Please enter password for tools page admin access.")

    # protect admin folder
    system("mkdir -p /usr/local/apache2/passwd/admintools")
    command = " ".join(['htdbm -bc /usr/local/apache2/passwd/admintools/passwords.dbm', username, password])
    system(command)

    # Adminer - Change cert to snakeoil cert.
    system("sed -i 's|^SSLCertificateFile /etc/ssl/certs/cert.pem|SSLCertificateFile /etc/ssl/certs/ssl-cert-snakeoil.pem\rSSLCertificateKeyFile /etc/ssl/private/ssl-cert-snakeoil.key|' /etc/adminer/apache.conf")

    # Webmin - Change cert to snakeoil cert.
    system("sed -i 's|^SSLCertificateFile /etc/ssl/certs/cert.pem|SSLCertificateFile /etc/ssl/certs/ssl-cert-snakeoil.pem\rSSLCertificateKeyFile /etc/ssl/private/ssl-cert-snakeoil.key|' /etc/webmin/miniserv.conf")

if __name__ == "__main__":
    main()

