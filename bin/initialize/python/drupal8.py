#!/usr/bin/python
# Copyright (C) 2018 Sean Borman <bormanst@gmail.com>.
# You should have received LICENSE.txt, a copy of the
# GNU General Public License, along with this program.
# If not, see <https://www.gnu.org/licenses/>.

"""

Set admin passwords, emails, and host data

"""

import MySQLdb as mdb
import os
import pwd
import string

from local_methods import *

DEFAULT_DIALOG_HEADER = "FormaVid - First boot configuration"
DEFAULT_HOSTNAME = "examplesitename.com"

def main():
    # Get envars.
    dbpass = os.environ.get("DB_PASS")
    email = os.environ.get("APP_EMAIL")
    hostname = os.environ.get("APP_HOSTNAME")
    password = os.environ.get("APP_PASS")

    # set vars
    d = Dialog(DEFAULT_DIALOG_HEADER)
    drupaldir = "/var/www/drupal8"
    username = "admin"

    if not hostname: hostname = DEFAULT_HOSTNAME

    if not password:
        password = d.get_password(
            "Drupal admin and cssadmin password",
            "Please enter password for Drupal admin and cssadmin accounts.")

    if not email:
        email = d.get_email(
            "Drupal admin Email",
            "Please enter email address for the Drupal admin account.",
            "%s@%s" % (username, hostname))

    if not dbpass:
        dbpass = d.get_input(
            "MySQL 'root' password",
            "Please enter new password for the MySQL 'root' account.")

    # Drupal - check change admin/password.
    con = ""
    try:
        pwd.getpwnam('admin')
        system("echo admin:%s | chpasswd" % password)
        # Get db conection.
        con = mdb.connect(host="localhost", user="root", passwd="%s" % dbpass)
        # Get db cursor.
        cur = con.cursor()
        # Update mariaDB user passwords.
        cur.execute('SET PASSWORD FOR admin@localhost = PASSWORD("%s"); flush privileges;' % password)
        cur.execute('SET PASSWORD FOR drupal8@localhost = PASSWORD("%s"); flush privileges;' % password)
        # Update email.
        cur.execute('UPDATE drupal8.users_field_data SET mail=\"%s\" WHERE name=\"admin\";' % email)
        cur.execute('UPDATE drupal8.users_field_data SET init=\"%s\" WHERE name=\"admin\";' % email)
        # Update site db access password.
        system('sed -i "s/\'password\' =>\(.*\)/\'password\' => \'%s\',/" %s/sites/%s/settings.php' % (password, drupaldir, hostname))
        # Update site admin password.
        system('drush -r %s -l https://%s user-password admin --password="%s"' % (drupaldir, hostname, password))
        # Clear site cache.
        system('drush -r %s -l https://%s cache-rebuild' % (drupaldir, hostname))
        # restart apache2
        system('systemctl restart apache2')
    except KeyError:
        # Error admin.
        system("")
        system("echo 'Unable to update password for admin. Ensure admin account exists.'")
        system("")
    finally:
        if con:
            con.close()

    # Drupal - check change cssadmin/password with toggle to create base site.
    try:
        # Check cssadmin exists with exception if not.
        pwd.getpwnam('cssadmin')
        # Change cssadmin password.
        system("echo cssadmin:%s | chpasswd" % password)
    except KeyError:
        # Error cssadmin.
        system("")
        system("echo 'Unable to update password for cssadmin. Ensure cssadmin account exists.'")
        system("")

if __name__ == "__main__":
    main()
