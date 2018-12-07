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
DEFAULT_HOSTNAME="examplesitename.com"

def main():
    # Get envars.
    apachepass = os.environ.get("INVOICENINJA_PASS")
    dbpass = os.environ.get("DB_PASS")
    email = os.environ.get("APP_EMAIL")
    hostname = os.environ.get("APP_HOSTNAME")
    password = os.environ.get("INVOICENINJA_PASS")
    update_email = os.environ.get("UPDATE_EMAIL")

    # set vars
    d = Dialog(DEFAULT_DIALOG_HEADER)
    username = "invoiceninja"
    restart_apache = False

    # Set hostname.
    if not hostname: hostname = DEFAULT_HOSTNAME

    # Check password.
    if not password:
        restart_apache = True
        password = d.get_password(
            "Invoice Ninja admin Password",
            "Enter password for the Invoice Ninja apache site access and admin account.")

    # Check dbpass.
    if not dbpass:
        dbpass = d.get_password(
            "MySQL 'root' Password",
            "Please enter new password for the MySQL 'root' account.")

    # Check apachepass.
    if not apachepass:
        restart_apache = True
        apachepass = d.get_password(
            "Apache access password",
            "Please enter password for Apache access to Invoice Ninja.")

    # Check update_email.
    if not update_email and not email:
        update_email = d.yesno(
            "Invoice Ninja admin Email",
            "Change the admin email for Invoice Ninja?",
            "Yes",
            "No")
        if update_email:
            # Get email.
            email = d.get_email(
                "Invoice Ninja admin Email",
                "Enter email address for the Invoice Ninja admin account.",
                "%s@%s" (username, hostname))
    # if email do update
    elif email: update_email = True
    # no email no update
    else: update_email = False

    # Set hashpass.
    hashpass = hashlib.md5(password).hexdigest()

    # Init db connection.
    con = ""
    try:
        # Get db conection.
        # con = mdb.connect(host="localhost", user="root", passwd="%s" % dbpass)
        # Get db cursor.
        # cur = con.cursor()
        # Update invoiceninja password.
        # cur.execute("ALTER USER invoiceninja@localhost IDENTIFIED BY '%s'; FLUSH PRIVILEGES;" % password)
        # Check update email.
        # Example ONLY - if update_email: cur.execute('UPDATE invoiceninja.user SET email=\"%s\" WHERE id=1;' % email)
        # Set apache2 htdbm password.
        directory = "/usr/local/apache2/passwd/invoiceninja"
        if os.path.isdir(directory): system("rm -rf %s" % directory)
        system("mkdir -p %s" % directory)
        directory = "".join([directory, '/passwords.dbm'])
        command = " ".join(['htdbm -bc', directory, username, apachepass])
        system(command)
        # restart apache2
        if restart_apache: system('systemctl restart apache2')
    except mdb.Error, e:
        print "Error %d: %s" % (e.args[0],e.args[1])
        sys.exit(1)
    finally:
        if con:
            con.close()

if __name__ == "__main__":
    main()
