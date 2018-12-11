#!/usr/bin/python
# Copyright (C) 2018 Sean Borman <bormanst@gmail.com>.
# You should have received LICENSE.txt, a copy of the
# GNU General Public License, along with this program.
# If not, see <https://www.gnu.org/licenses/>.

"""

Set Solr password

"""

import os

from dialog_wrapper import Dialog
from local_methods import *

DEFAULT_DIALOG_HEADER = "FormaVid - First boot configuration"

def main():
    # Get envars.
    solrnew = os.environ.get("SOLR_NEW")
    solrold = os.environ.get("SOLR_OLD")

    # Set vars.
    d = Dialog(DEFAULT_DIALOG_HEADER)

    # Check solr running.
    out = system("systemctl is-active solr")
    if out and out.strip().lower() != 'active':
        system("echo ''")
        system("echo 'Solr service is not active.'")
        system("echo 'Please ensure Solr service is running prior to changing passwords.'")
        system("echo ''")
        quit()

    # Check solrold.
    if not solrold:
        solrold = d.get_password(
            "Old Solr 'admin' password",
            "Please enter OLD password for Solr access.")

    # Check solrnew.
    if not solrnew:
        restart_solr = True
        solrnew = d.get_password(
            "New Solr 'admin' password",
            "Please enter NEW password for Solr access.")

    # Change non-admin passwords first.
    system('curl -k --user admin:%s http://localhost:8983/solr/admin/authentication -H "Content-type:application/json" -d "{\"set-user\": {\"drupal8\":\"%s\"}}"' % (solrold, solrnew))

    # Change admin password last.
    system('curl -k --user admin:%s http://localhost:8983/solr/admin/authentication -H "Content-type:application/json" -d "{\"set-user\": {\"admin\":\"%s\"}}"' % (solrold, solrnew))

    # Apply changes.
    system('systemctl restart solr')

if __name__ == "__main__":
    main()
