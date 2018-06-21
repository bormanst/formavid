#!/usr/bin/python
# Copyright (C) 2018 Sean Borman <bormanst@gmail.com>.
# You should have received LICENSE.txt, a copy of the
# GNU General Public License, along with this program.
# If not, see <https://www.gnu.org/licenses/>.

"""

Set admin passwords, emails, and host data

"""

import os
import pwd
import string

from mysqlconf import MySQL
from local_methods import *

def main():
    # Get envars.
    adminpass = os.environ.get("APP_PASS")
    formavid = os.environ.get("FORMAVID")

    # Borgbackup password.
    system("python %s/bin/initialize/python/borgbackup.py" % formavid)

    # Roundup password.
    system("python %s/bin/initialize/python/roundup.py" % formavid)

    # Simple Invoices password.
    system("python %s/bin/initialize/python/simpleinvoices.py" % formavid)

    # Tools password.
    system("python %s/bin/initialize/python/tools.py" % formavid)

    # Drupal - check change admin/password.
    try:
        pwd.getpwnam('admin')
        system("echo admin:%s | chpasswd" % adminpass)
        m = MySQL()
        m.execute('SET PASSWORD FOR drupal8@localhost = PASSWORD(%s);' % adminpass)
    except KeyError:
        # Error admin.
        system("")
        system("echo 'Unable to update password for admin. Ensure admin account exists.'")
        system("")

    # Drupal - check change cssadmin/password with toggle to create base site.
    try:
        # Check cssadmin exists with exception if not.
        pwd.getpwnam('cssadmin')
        # Change cssadmin password.
        system("echo cssadmin:%s | chpasswd" % adminpass)
    except KeyError:
        # Error cssadmin.
        system("")
        system("echo 'Unable to update password for cssadmin. Ensure cssadmin account exists.'")
        system("")

    # restart apache2
    system('systemctl restart apache2')

if __name__ == "__main__":
    main()
