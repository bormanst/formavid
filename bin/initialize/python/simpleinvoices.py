#!/usr/bin/python
# Copyright (C) 2018 Sean Borman <bormanst@gmail.com>.
# You should have received LICENSE.txt, a copy of the
# GNU General Public License, along with this program.
# If not, see <https://www.gnu.org/licenses/>.

"""

Set SimpleInvoices admin password and email

"""

import hashlib
import MySQLdb as mdb
import os

from dialog_wrapper import Dialog
from local_methods import *

DEFAULT_DIALOG_HEADER = "FormaVid - First boot configuration"

def main():
    # Get envars.
    apachepass = os.environ.get("TOOLS_PASS")
    dbpass = os.environ.get("DB_PASS")
    email = os.environ.get("APP_EMAIL")
    password = os.environ.get("SIMPLEINVOICES_PASS")
    update_email = os.environ.get("UPDATE_EMAIL")

    # set vars
    d = Dialog(DEFAULT_DIALOG_HEADER)
    username = "admin"

    if not update_email: update_email = False
    else: update_email = True

    if not password:
        password = d.get_password(
            "Simple Invoices admin Password",
            "Enter password for the Simple Invoices apache site access and admin account.")

    if not dbpass:
        dbpass = d.get_password(
            "MySQL 'root' Password",
            "Please enter new password for the MySQL 'root' account.")

    if not apachepass:
        apachepass = d.get_password(
            "Apache access password",
            "Please enter password for Apache access to Simple Invoices.")

    if not email:
        # Check need update email.
        update_email = not d.yesno(
            "Change email",
            "Do you wish to change the Simple Invoices admin email?",
            "No",
            "Yes")
        # Check update email.
        if update_email:
            # Get email.
            email = d.get_email(
                "Simple Invoices admin Email",
                "Enter email address for the Simple Invoices admin account.")

    hashpass = hashlib.md5(password).hexdigest()

    con = ""
    try:
        # Get db conection.
        con = mdb.connect(host="localhost", user="root", passwd="%s" % dbpass)
        # Get db cursor.
        cur = con.cursor()
        # Update simpleinvoices password.
        cur.execute('SET PASSWORD FOR simpleinvoices@localhost = PASSWORD("%s"); flush privileges;' % password)
        cur.execute('UPDATE simpleinvoices.si_user SET password=\"%s\" WHERE id=1;' % hashpass)
        # Check update email.
        if update_email: cur.execute('UPDATE simpleinvoices.si_user SET email=\"%s\" WHERE id=1;' % email)
        system('sed -i "0,/params.password/s/params.password.*/params.password = %s/" /var/www/simpleinvoices/config/config.php' % password)
        system("sed -i 's|^encryption.default.key.*|encryption.default.key = %s|' /var/www/simpleinvoices/config/config.php" % password)
        # Set apache2 htdbm password.
        directory = "/usr/local/apache2/passwd/simpleinvoices"
        if os.path.isdir(directory): system("rm -rf %s" % directory)
        system("mkdir -p %s" % directory)
        directory = "".join([directory, '/passwords.dbm'])
        command = " ".join(['htdbm -bc', directory, username, apachepass])
        system(command)
        # restart apache2
        system('systemctl restart apache2')
    except mdb.Error, e:
        print "Error %d: %s" % (e.args[0],e.args[1])
        sys.exit(1)
    finally:
        if con:
            con.close()

if __name__ == "__main__":
    main()
