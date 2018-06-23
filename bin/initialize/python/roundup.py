#!/usr/bin/python
# Copyright (C) 2018 Sean Borman <bormanst@gmail.com>.
# You should have received LICENSE.txt, a copy of the
# GNU General Public License, along with this program.
# If not, see <https://www.gnu.org/licenses/>.

"""

Set Roundup admin password and email

"""

import hashlib
import MySQLdb as mdb
import os

from dialog_wrapper import Dialog
from local_methods import *

DEFAULT_DIALOG_HEADER = "FormaVid - First boot configuration"

def main():
    username = "admin"

    dbpass = os.environ.get("DB_PASS")
    email = os.environ.get("APP_EMAIL")
    hostname = os.environ.get("APP_HOSTNAME")
    password = os.environ.get("ROUNDUP_PASS")

    d = Dialog(DEFAULT_DIALOG_HEADER)

    if not password:
        password = d.get_password(
            "Roundup admin password",
            "Please enter password for the Roundup admin account.")

    if not email:
        email = d.get_email(
            "Roundup admin Email",
            "Please enter email address for the Roundup admin account.",
            "admin@example.com")

    if not dbpass:
        dbpass = d.get_input(
            "MySQL 'root' password",
            "Please enter new password for the MySQL 'root' account.")

    hashpass = "{SHA}" + hashlib.sha1(password).hexdigest()

    con = ""
    try:
        # Get db conection.
        con = mdb.connect(host="localhost", user="root", passwd="%s" % dbpass)
        # Get db cursor.
        cur = con.cursor()
        # Update email and password.
        cur.execute('SET PASSWORD FOR roundup@localhost = PASSWORD("%s"); flush privileges;' % password)
        cur.execute('UPDATE roundup._user SET _password=\"%s\" WHERE _username=\"admin\";' % hashpass)
        cur.execute('UPDATE roundup._user SET _address=\"%s\" WHERE _username=\"admin\";' % email)
    except mdb.Error, e:
        print "Error %d: %s" % (e.args[0],e.args[1])
        sys.exit(1)
    finally:
        if con:
            con.close()

    # Set tacker config password.
    system("sed -i 's/^password = \(.*\)/password = %s/' /etc/roundup/tracker-config.ini" % password)

    # Set apache2 htdbm password.
    # directory = "/usr/local/apache2/passwd/roundup"
    # if not os.path.isdir(directory): system("mkdir -p %s" % directory)
    # directory = "".join([directory, '/passwords.dbm'])
    # command = " ".join(['htdbm -bc', directory, username, password])
    # system(command)

    # restart apache2
    system('systemctl restart apache2')

if __name__ == "__main__":
    main()

