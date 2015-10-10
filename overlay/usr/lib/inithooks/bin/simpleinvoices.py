#!/usr/bin/python
"""Set SimpleInvoices admin password and email

Option:
    --pass=     unless provided, will ask interactively
    --email=    unless provided, will ask interactively

"""

import sys
import getopt
import hashlib

from dialog_wrapper import Dialog
from mysqlconf import MySQL
from executil import system

def usage(s=None):
    if s:
        print >> sys.stderr, "Error:", s
    print >> sys.stderr, "Syntax: %s [options]" % sys.argv[0]
    print >> sys.stderr, __doc__
    sys.exit(1)

def main():
    try:
        opts, args = getopt.gnu_getopt(sys.argv[1:], "h",
                                       ['help', 'pass=', 'email='])
    except getopt.GetoptError, e:
        usage(e)

    password = ""
    email = ""
    username = "admin"

    for opt, val in opts:
        if opt in ('-h', '--help'):
            usage()
        elif opt == '--pass':
            password = val
        elif opt == '--email':
            email = val

    if not password:
        d = Dialog('TurnKey Linux - First boot configuration')
        password = d.get_password("Simple Invoices admin Password", "Enter password for the Simple Invoices apache site access and admin account.")

    if not email:
        if 'd' not in locals():
            d = Dialog('TurnKey Linux - First boot configuration')

        email = d.get_email("Simple Invoices admin Email", "Enter email address for the Simple Invoices admin account.", "admin@example.com")

    hash = hashlib.md5(password).hexdigest()

    m = MySQL()
    m.execute('UPDATE simpleinvoices.si_user SET password=\"%s\" WHERE id=1;' % hash)
    m.execute('UPDATE simpleinvoices.si_user SET email=\"%s\" WHERE id=1;' % email)

    # protect admin folder
    system("mkdir -p /usr/local/apache2/passwd/simpleinvoices")
    command = " ".join(['htdbm -bc /usr/local/apache2/passwd/simpleinvoices/passwords.dbm', username, password])
    system(command)

if __name__ == "__main__":
    main()

