#!/usr/bin/python
# Copyright (C) 2018 Sean Borman <bormanst@gmail.com>.
# You should have received LICENSE.txt, a copy of the
# GNU General Public License, along with this program.
# If not, see <https://www.gnu.org/licenses/>.

"""

Set drupal8 admin email address for all sites.

"""

import os
import string

from dialog_wrapper import Dialog
from local_methods import *

DEFAULT_DIALOG_HEADER = "FormaVid - First boot configuration"
DEFAULT_HOSTNAME = "examplesitename.com"

def get_immediate_subdirectories(a_dir):
    return [name for name in os.listdir(a_dir)
            if os.path.isdir(os.path.join(a_dir, name))]

def main():
    # Get envars.
    email = os.environ.get("APP_EMAIL")
    hostname = os.environ.get("APP_HOSTNAME")

    # Set hostname.
    if not hostname: hostname = DEFAULT_HOSTNAME

    # Set vars.
    d = Dialog(DEFAULT_DIALOG_HEADER)
    drupaldir = "/var/www/drupal8"
    username = "admin"
    sitename = sitename = get_sitename(hostname)

    # Check email.
    if not email or email == "None":
        # Get email.
        email = d.get_email(
            "Drupal 'admin' Email",
            "Please enter email address for all Drupal 'admin' accounts.",
            "%s@%s" % (username, hostname))

    # Cycle through /var/www/drupal8/sites.
    sites_dir = "/".join([drupaldir, 'sites'])
    if os.path.exists(sites_dir):
        sites = get_immediate_subdirectories(sites_dir)
        for site in sites:
            # Skip default directory.
            if "default" not in site:
                # Show which site.
                system("echo 'Updating: %s'" % site)
                # Update email.
                system('drush -r %s -l https://%s sql:query "UPDATE users_field_data SET mail=\'%s\' WHERE name=\'admin\';"' % (drupaldir, site, email))
                # Clear site cache.
                system("drupal --root=%s --uri=\"http://%s\" cache:rebuild" % (drupaldir, site))

    system("echo 'Update drupal8 email for admin has completed.'")

if __name__ == "__main__":
    main()
