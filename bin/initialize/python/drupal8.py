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
DEFAULT_HOSTNAME = "examplesitename.com"

def escape_chars(s):
    """escape special characters: required by nested quotes in query"""
    s = s.replace("\\", "\\\\")  # \  ->  \\
    s = s.replace('"', '\\"')    # "  ->  \"
    s = s.replace("'", "'\\''")  # '  ->  '\''
    return s

def get_immediate_subdirectories(a_dir):
    return [name for name in os.listdir(a_dir)
            if os.path.isdir(os.path.join(a_dir, name))]

def main():
    # Get envars.
    dbpass = os.environ.get("DB_PASS")
    email = os.environ.get("APP_EMAIL")
    hostname = os.environ.get("APP_HOSTNAME")
    password = os.environ.get("APP_PASS")
    update_email = os.environ.get("UPDATE_EMAIL")

    # set vars
    d = Dialog(DEFAULT_DIALOG_HEADER)
    drupaldir = "/var/www/drupal8"
    username = "admin"
    restart_apache = False

    # Set hostname.
    if not hostname: hostname = DEFAULT_HOSTNAME

    # Check password.
    if not password:
        restart_apache = True
        password = d.get_password(
            "Drupal/MariaDb/System 'admin' and 'cssadmin' password",
            "Please enter password for Drupal 'admin' and 'cssadmin' accounts.")

    # Check dbpass.
    if not dbpass:
        dbpass = d.get_password(
            "Current MariaDb 'root' password",
            "Please enter current MariaDb 'root' password for db access.")

    # Check update_email.
    if not update_email and not email:
        update_email = d.yesno(
            "Drupal 'admin' Email",
            "Change the 'admin' email for Drupal site(s)?",
            "Yes",
            "No")
        if update_email:
            # Get email.
            email = d.get_email(
                "Drupal 'admin' Email",
                "Please enter email address for Drupal 'admin' account.",
                "%s@%s" % (username, hostname))
    # if email do update
    elif email: update_email = True
    # no email no update
    else: update_email = False

    # Init db connection.
    con = ""
    try:
        pwd.getpwnam('admin')
        system("echo admin:%s | chpasswd" % password)
        # Get db conection.
        con = mdb.connect(host="localhost", user="root", passwd="%s" % dbpass)
        # Get db cursor.
        cur = con.cursor()
        # Update mariaDB user passwords.
        cur.execute('SET PASSWORD FOR admin@localhost = PASSWORD("%s"); flush privileges;' % escape_chars(password))
        cur.execute('SET PASSWORD FOR drupal8@localhost = PASSWORD("%s"); flush privileges;' % escape_chars(password))
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
                system('drupal --root=%s --uri="http://%s" user:password:reset admin %s' % (drupaldir, site, password))
                # Check emails too.
                if update_email:
                    # Update email.
                    system('drush -r %s -l https://%s sql-query "UPDATE users_field_data SET mail=\'%s\' WHERE name=\'admin\';"' % (drupaldir, site, email))
                    system('drush -r %s -l https://%s sql-query "UPDATE users_field_data SET init=\'%s\' WHERE name=\'admin\';"' % (drupaldir, site, email))
                # Clear site cache.
                system("drupal --root=%s --uri=\"http://%s\" cache:rebuild" % (drupaldir, site))
        if restart_apache:
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

    # Check change cssadmin password.
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
