#!/usr/bin/python
# Copyright (C) 2018 Sean Borman <bormanst@gmail.com>.
# You should have received LICENSE.txt, a copy of the
# GNU General Public License, along with this program.
# If not, see <https://www.gnu.org/licenses/>.

"""

Set admin passwords

"""

import MySQLdb as mdb
import os
import pwd
import string

from dialog_wrapper import Dialog
from local_methods import *

DEFAULT_DIALOG_HEADER = "FormaVid - First boot configuration"

def get_immediate_subdirectories(a_dir):
    return [name for name in os.listdir(a_dir)
            if os.path.isdir(os.path.join(a_dir, name))]

def main():
    # Get envars.
    dbpass = os.environ.get("DB_PASS")
    email = os.environ.get("APP_EMAIL")
    password = os.environ.get("APP_PASS")

    # set vars
    d = Dialog(DEFAULT_DIALOG_HEADER)
    drupaldir = "/var/www/drupal8"
    update_email = False
    username = "admin"

    if not password:
        password = d.get_password(
            "Drupal admin and cssadmin password",
            "Please enter password for Drupal admin and cssadmin accounts.")

    if not dbpass:
        dbpass = d.get_password(
            "MySQL 'root' password",
            "Please enter new password for the MySQL 'root' account.")

    if not email:
        # Check need update email.
        update_email = not d.yesno(
            "Change email",
            "Do you wish to change the drupal admin email?",
            "No",
            "Yes")
        if update_email:
            # Get email.
            email = d.get_email(
                "Drupal admin Email",
                "Please enter email address for the Drupal admin account.")

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
        # Cycle through /var/www/drupal8/sites.
        sites_dir = "/".join([drupaldir, 'sites'])
        sites = get_immediate_subdirectories(sites_dir)
        for site in sites:
            # Skip default directory.
            if "default" not in site:
                # Show which site.
                system("echo 'Updating: %s'" % site)
                # Update site db access password.
                system('sed -i "s/\'password\' =>\(.*\)/\'password\' => \'%s\',/" %s/sites/%s/settings.php' % (password, drupaldir, site))
                # Update site admin password.
                system('drush -r %s -l https://%s user-password admin --password="%s"' % (drupaldir, site, password))
                # Check emails too.
                if update_email:
                    # Update email.
                    system('drush -r %s -l https://%s sql-query "UPDATE users_field_data SET mail=\'%s\' WHERE name=\'admin\';"' % (drupaldir, site, email))
                    system('drush -r %s -l https://%s sql-query "UPDATE users_field_data SET init=\'%s\' WHERE name=\'admin\';"' % (drupaldir, site, email))
                # Clear site cache.
                system('drush -r %s -l https://%s cache-rebuild' % (drupaldir, site))
        # restart apache2
        system('systemctl restart apache2')
        system("echo 'Update password for admin has completed. Service apache2 has been restarted.'")
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
        system("echo 'Update password for cssadmin has completed.'")
    except KeyError:
        # Error cssadmin.
        system("")
        system("echo 'Unable to update password for cssadmin. Ensure cssadmin account exists.'")
        system("")

if __name__ == "__main__":
    main()
