#!/usr/bin/python
# Copyright (C) 2018 Sean Borman <bormanst@gmail.com>.
# You should have received LICENSE.txt, a copy of the
# GNU General Public License, along with this program.
# If not, see <https://www.gnu.org/licenses/>.

"""

Set Roundup admin password.

"""

import MySQLdb as mdb
import os

from dialog_wrapper import Dialog
from local_methods import *

DEFAULT_DIALOG_HEADER = "FormaVid - First boot configuration"

def main():
    # Get envars.
    dbpass = os.environ.get("DB_PASS")
    password = os.environ.get("ROUNDUP_PASS")

    # set vars
    d = Dialog(DEFAULT_DIALOG_HEADER)
    tracker="support"
    username = "admin"

    if not password:
        password = d.get_password(
            "Roundup 'admin' password",
            "Please enter password for Roundup 'admin' and MariaDb account.")

    if not dbpass:
        dbpass = d.get_input(
            "MariaDb 'root' password",
            "Please enter password for MariaDb 'root' account.")

    con = ""
    try:
        # Get db conection.
        con = mdb.connect(host="localhost", user="root", passwd="%s" % dbpass)
        # Get db cursor.
        cur = con.cursor()
        # Update mariaDB user password.
        system("echo 'Updating MariaDb roundup password ...'")
        cur.execute('SET PASSWORD FOR roundup@localhost = PASSWORD("%s"); flush privileges;' % password)
        # Set tracker db access password.
        system("echo 'Updating Roundup support tracker password ...'")
        system("sed -i 's/^password = \(.*\)/password = %s/' /etc/roundup/%s/tracker-config.ini" % (password, tracker))
        # Update tracker admin password.
        system("echo 'Updating Roundup admin password ...'")
        system('roundup-admin -i /var/www/%s set user1 password="%s"' % (tracker, password))
    except mdb.Error, e:
        print "Error %d: %s" % (e.args[0],e.args[1])
        sys.exit(1)
    finally:
        if con:
            con.close()

if __name__ == "__main__":
    main()
