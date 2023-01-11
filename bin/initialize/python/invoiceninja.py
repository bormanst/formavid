#!/usr/bin/python
# Copyright (C) 2018 Sean Borman <bormanst@gmail.com>.
# You should have received LICENSE.txt, a copy of the
# GNU General Public License, along with this program.
# If not, see <https://www.gnu.org/licenses/>.

"""

Set Invoice Ninja admin password

"""

import hashlib
import MySQLdb as mdb
import os

from dialog_wrapper import Dialog
from local_methods import *

DEFAULT_DIALOG_HEADER = "FormaVid - First boot configuration"

def escape_chars(s):
    """escape special characters: required by nested quotes in query"""
    s = s.replace("\\", "\\\\")  # \  ->  \\
    s = s.replace('"', '\\"')    # "  ->  \"
    s = s.replace("'", "'\\''")  # '  ->  '\''
    return s

def main():
    # Get envars.
    apachepass = os.environ.get("INVOICENINJA_PASS")
    dbpass = os.environ.get("DB_PASS")
    password = os.environ.get("INVOICENINJA_PASS")

    # set vars
    d = Dialog(DEFAULT_DIALOG_HEADER)
    env_file = "/var/www/invoiceninja/.env"
    restart_apache = False
    username = "invoiceninja"

    # Check password.
    if not password:
        restart_apache = True
        password = d.get_password(
            "Invoice Ninja admin Password",
            "Enter password for the Invoice Ninja apache setup access and admin account.")

    # Check dbpass.
    if not dbpass:
        dbpass = d.get_password(
            "MariaDb 'root' password",
            "Please enter password for MariaDb 'root' account.")

    # Check apachepass.
    if not apachepass:
        restart_apache = True
        apachepass = d.get_password(
            "Apache access password",
            "Please enter password for Apache access to Invoice Ninja setup.")

    # Init db connection.
    con = ""
    try:
        # Get db conection.
        con = mdb.connect(host="localhost", user="root", passwd="%s" % dbpass)
        # Get db cursor.
        cur = con.cursor()
        # Update invoiceninja MariaDb password.
        system("echo 'Updating MariaDb invoiceninja password ...'")
        cur.execute('SET PASSWORD FOR invoiceninja@localhost = PASSWORD("%s"); FLUSH PRIVILEGES;' % escape_chars(password))
        # Update invoiceninja .env with MariaDb and Postfix password.
        system("echo 'Updating Invoice Ninja .env file MariaDb and Postfix passwords ...'")
        if os.path.exists(env_file):
            system("sed -i 's/^DB_PASSWORD=\(.*\)/DB_PASSWORD=%s/' %s" % (password, env_file))
            system("sed -i 's/^MAIL_PASSWORD=\(.*\)/MAIL_PASSWORD=%s/' %s" % (password, env_file))
        # Set apache2 htdbm password.
        system("echo 'Updating Apache2 invoiceninja password for setup access ...'")
        directory = "/usr/local/apache2/passwd/invoiceninja"
        if os.path.isdir(directory): system("rm -rf %s" % directory)
        system("mkdir -p %s" % directory)
        directory = "".join([directory, '/passwords.dbm'])
        command = " ".join(['htdbm -bc', directory, username, apachepass])
        system(command)
        # restart apache2
        if restart_apache: system('systemctl restart apache2')
    except mdb.Error as e:
        # print "Error %d: %s" % (e.args[0],e.args[1])
        sys.exit(1)
    finally:
        if con:
            con.close()

if __name__ == "__main__":
    main()
