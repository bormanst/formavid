#!/usr/bin/python
# Copyright (C) 2018 Sean Borman <bormanst@gmail.com>.
# You should have received LICENSE.txt, a copy of the
# GNU General Public License, along with this program.
# If not, see <https://www.gnu.org/licenses/>.

"""

Set password for the drupal8 account access to Solr.

"""

import os
import string

from dialog_wrapper import Dialog
from local_methods import *

DEFAULT_DIALOG_HEADER = "FormaVid - First boot configuration"

def get_immediate_subdirectories(a_dir):
    return [name for name in os.listdir(a_dir) if os.path.isdir(os.path.join(a_dir, name))]

def main():
    # Get envars.
    solrnew = os.environ.get("SOLR_NEW")

    # Set vars.
    d = Dialog(DEFAULT_DIALOG_HEADER)
    drupaldir = "/var/www/drupal8"

    if not solrnew or solrnew == "None":
        solrnew = d.get_password(
            "Drupal8 Solr server access.",
            "Please enter Solr password for the drupal8 account access.")

    # Cycle through /var/www/drupal8/sites.
    sites_dir = "/".join([drupaldir, 'sites'])
    if os.path.exists(sites_dir):
        sites = get_immediate_subdirectories(sites_dir)
        for site in sites:
            # Skip default directory.
            if "default" not in site:
                # Show which site.
                system("echo 'Updating: %s'" % site)
                # Update solr access password.
                system("drush -r %s -l http://%s config:set -y search_api.server.%s_solr_server backend_config.connector_config.password %s" % (drupaldir, baseUri, get_sitename(site), solrnew))
                # Clear site cache.
                system("drupal --root=%s --uri=\"http://%s\" cache:rebuild" % (drupaldir, site))

    system("echo 'Update password for Drupal8 Solr access has completed.'")

if __name__ == "__main__":
    main()
