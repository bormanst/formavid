#!/usr/bin/python
# Copyright (C) 2018 Sean Borman <bormanst@gmail.com>.
# You should have received LICENSE.txt, a copy of the
# GNU General Public License, along with this program.
# If not, see <https://www.gnu.org/licenses/>.

"""

Set admin system and drupal9 passwords.

"""

import MySQLdb as mdb
import os
import pwd
import string

from dialog_wrapper import Dialog
from local_methods import *

def escape_chars(s):
    """escape special characters: required by nested quotes in query"""
    s = s.replace("\\", "\\\\")  # \  ->  \\
    s = s.replace('"', '\\"')    # "  ->  \"
    s = s.replace("'", "'\\''")  # '  ->  '\''
    return s

def get_immediate_subdirectories(a_dir):
    return [name for name in os.listdir(a_dir) if os.path.isdir(os.path.join(a_dir, name))]

DEFAULT_DIALOG_HEADER = "FormaVid - First boot configuration"

def main():
    # Get envars.
    dbpass = os.environ.get("DB_PASS")
    password = os.environ.get("APP_PASS")
    sync_cssadmin = os.environ.get("SYNC_CSSADMIN")

    # Set vars.
    d = Dialog(DEFAULT_DIALOG_HEADER)
    drupaldir = "/var/www/drupal9"
    username = "admin"
    restart_apache = False
    update_cssadmin = False

    # Check password.
    if not password or password == "None":
        restart_apache = True
        password = d.get_password(
            "Drupal9/MariaDb/System 'admin' password",
            "Please enter password for 'admin' account.")

    # Check dbpass.
    if not dbpass or dbpass == "None":
        dbpass = d.get_password(
            "Current MariaDb 'root' password",
            "Please enter current MariaDb 'root' password for db access.")

    # Check sync_cssadmin.
    if not sync_cssadmin or sync_cssadmin == "None":
        update_cssadmin = d.yesno(
            "Sync 'cssadmin' system password",
            "Sync the 'cssadmin' password with 'admin' account?",
            "Yes",
            "No")
    elif sync_cssadmin == "True": update_cssadmin = True

    # Init db connection.
    con = ""
    try:
        pwd.getpwnam('admin')
        system("echo 'Updating system admin password ...'")
        system("echo admin:%s | chpasswd" % password)
        # Get db conection.
        con = mdb.connect(host="localhost", user="root", passwd="%s" % dbpass)
        # Get db cursor.
        cur = con.cursor()
        # Update mariaDB user passwords.
        system("echo 'Updating MariaDb admin password ...'")
        cur.execute('SET PASSWORD FOR admin@localhost = PASSWORD("%s"); flush privileges;' % escape_chars(password))
        system("echo 'Updating MariaDb drupal9 password ...'")
        cur.execute('SET PASSWORD FOR drupal9@localhost = PASSWORD("%s"); flush privileges;' % escape_chars(password))
        # Cycle through /var/www/drupal9/sites.
        sites_dir = "/".join([drupaldir, 'sites'])
        if os.path.exists(sites_dir):
            sites = get_immediate_subdirectories(sites_dir)
            for site in sites:
                # Skip default directory.
                if "default" not in site:
                    # Show which site.
                    system("echo 'Updating: %s'" % site)
                    # Update site db access password.
                    system("echo 'Updating MariaDb password in Drupal9 settings.php files ...'")
                    system('sed -i "s/\'password\' =>\(.*\)/\'password\' => \'%s\',/" %s/sites/%s/settings.php' % (password, drupaldir, site))
                    # Update site admin password.
                    system("echo 'Updating Drupal9 admin password for sites access ...'")
                    system('drupal --root=%s --uri="http://%s" user:password:reset admin %s' % (drupaldir, site, password))
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
    if update_cssadmin:
        try:
            # Check cssadmin exists with exception if not.
            pwd.getpwnam('cssadmin')
            # Change cssadmin password.
            system("echo 'Updating system cssadmin password ...'")
            system("echo cssadmin:%s | chpasswd" % password)
        except KeyError:
            # Error cssadmin.
            system("")
            system("echo 'Unable to update password for cssadmin. Ensure cssadmin account exists.'")
            system("")

if __name__ == "__main__":
    main()
