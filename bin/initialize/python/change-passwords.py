#!/usr/bin/python
# Copyright (C) 2018 Sean Borman <bormanst@gmail.com>.
# You should have received LICENSE.txt, a copy of the
# GNU General Public License, along with this program.
# If not, see <https://www.gnu.org/licenses/>.

"""

Change passwords for appliance.

"""

import os
import string

from dialog_wrapper import Dialog
from local_methods import *

DEFAULT_DIALOG_HEADER = "FormaVid - First boot configuration"

def main():
    # Assign common dialog header.
    d = Dialog(DEFAULT_DIALOG_HEADER)

    # Set envars.
    formavid = "/usr/local/formavid"
    if os.environ.get("FORMAVID"): formavid = os.environ.get("FORMAVID")

    # Check use singl password.
    single_pass = os.environ.get("SINGLE_PASS")

    # Set passwords.
    if single_pass and not single_pass == "None":
        # Use same password.
        system("echo 'Setting password envars to single password ...'")
        os.environ["APP_PASS"] = single_pass
        os.environ["DB_PASS"] = single_pass
        os.environ["INVOICENINJA_PASS"] = single_pass
        os.environ["ROUNDUP_PASS"] = single_pass
        os.environ["SOLR_NEW"] = single_pass
        os.environ["TOOLS_PASS"] = single_pass
        os.environ["WEBMIN_PASS"] = single_pass

    # Change system and db passwords first.
    system("echo 'Updating the appliance passwords ...'")

    # Webmin password.
    system("python %s/bin/initialize/python/webmin.py" % formavid)

    # MariaDB password.
    system("python %s/bin/initialize/python/mysqlconf.py" % formavid)

    # Drupal password.
    system("python %s/bin/initialize/python/drupal8.py" % formavid)

    # Invoice Ninja password.
    system("python %s/bin/initialize/python/invoiceninja.py" % formavid)

    # Roundup password.
    system("python %s/bin/initialize/python/roundup.py" % formavid)

    # Solr password.
    solr_install = os.environ.get("SOLR_INSTALL")
    solrold = os.environ.get("SOLR_OLD")
    if solr_install and solr_install == "True" and solrold and not solrold == "None":
        system("python %s/bin/initialize/python/solr.py" % formavid)

    # Tools password.
    system("python %s/bin/initialize/python/tools.py" % formavid)

    system("echo 'Finished updating the appliance passwords.'")

if __name__ == "__main__":
    main()
