#!/usr/bin/python
# Copyright (C) 2018 Sean Borman <bormanst@gmail.com>.
# You should have received LICENSE.txt, a copy of the
# GNU General Public License, along with this program.
# If not, see <https://www.gnu.org/licenses/>.

"""

Set Roundup admin password and email

"""

import MySQLdb as mdb
import os

from dialog_wrapper import Dialog
from local_methods import *

DEFAULT_DIALOG_HEADER = "FormaVid - First boot configuration"
DEFAULT_HOSTNAME = "examplesitename.com"

def main():
    # Get envars.
    apachepass = os.environ.get("TOOLS_PASS")
    dbpass = os.environ.get("DB_PASS")
    email = os.environ.get("APP_EMAIL")
    hostname = os.environ.get("APP_HOSTNAME")
    password = os.environ.get("ROUNDUP_PASS")

    # set vars
    d = Dialog(DEFAULT_DIALOG_HEADER)
    username = "admin"

    if not hostname: hostname = DEFAULT_HOSTNAME

    if not password:
        password = d.get_password(
            "Roundup admin password",
            "Please enter password for the Roundup admin account.")

    if not email:
        email = d.get_email(
            "Roundup admin Email",
            "Please enter email address for the Roundup admin account.",
            "%s@%s" % (username, hostname))

    if not dbpass:
        dbpass = d.get_input(
            "MySQL 'root' password",
            "Please enter new password for the MySQL 'root' account.")

    if not apachepass:
        apachepass = d.get_password(
            "Apache access password",
            "Please enter password for Apache access to Roundup.")

    con = ""
    try:
        # Get db conection.
        con = mdb.connect(host="localhost", user="root", passwd="%s" % dbpass)
        # Get db cursor.
        cur = con.cursor()
        # Update mariaDB user password.
        cur.execute('SET PASSWORD FOR roundup@localhost = PASSWORD("%s"); flush privileges;' % password)
        # Set tracker db access password.
        system("sed -i 's/^password = \(.*\)/password = %s/' /etc/roundup/tracker-config.ini" % password)
        # Update tracker admin password.
        system('roundup-admin -i /var/www/support set user1 password="%s"' % password)
        # Update tracker admin email.
        system('roundup-admin -i /var/www/support set user1 address="%s"' % email)
        # Set apache2 htdbm password.
        directory = "/usr/local/apache2/passwd/roundup"
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

