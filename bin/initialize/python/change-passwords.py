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
    if not single_pass:
        use_single_pass = d.yesno(
            "Single password option",
            "Use the same password for everything (not Single Sign On)?",
            "Yes",
            "No")
        if use_single_pass:
            single_pass = d.get_password(
                "Use single password for system",
                "Please enter password for all system access (not SSO).")

    # Set passwords.
    if single_pass:
        # Use same password.
        system("echo 'Setting password envars to single password ...'")
        os.environ["APP_PASS"] = single_pass
        os.environ["DB_PASS"] = single_pass
        os.environ["INVOICENINJA_PASS"] = single_pass
        os.environ["ROUNDUP_PASS"] = single_pass
        os.environ["SOLR_NEW"] = single_pass
        os.environ["TOOLS_PASS"] = single_pass
        os.environ["WEBMIN_PASS"] = single_pass
    else:
        # Use different passwords.
        if not os.environ.get("WEBMIN_PASS"):
            os.environ["WEBMIN_PASS"] = d.get_password(
                "Webmin and System 'root' password",
                "Please enter password for Webmin 'root' access and system account.")

        if not os.environ.get("DB_PASS"):
            os.environ["DB_PASS"] = d.get_password(
                "MariaDb 'root' password",
                "Please enter password for MariaDb 'root' account.")

        if not os.environ.get("APP_PASS"):
            os.environ["APP_PASS"] = d.get_password(
                "Drupal/MariaDb/Solr/System 'admin' and 'cssadmin' password",
                "Please enter password for Drupal 'admin' and 'cssadmin' accounts.")

        if not os.environ.get("SOLR_NEW"):
            os.environ["SOLR_NEW"] = d.get_password(
                "New Solr 'admin' password",
                "Please enter NEW password for Solr access.")

        if not os.environ.get("SOLR_OLD"):
            os.environ["SOLR_OLD"] = d.get_password(
                "Old Solr 'admin' password",
                "Please enter OLD password for Solr access.")

        if not os.environ.get("INVOICENINJA_PASS"):
            os.environ["INVOICENINJA_PASS"] = d.get_password(
                "Invoice Ninja 'admin' password",
                "Please enter password for Invoice Ninja setup and MariaDb account.")

        if not os.environ.get("ROUNDUP_PASS"):
            os.environ["ROUNDUP_PASS"] = d.get_password(
                "Roundup 'admin' password",
                "Please enter password for Roundup 'admin' and MariaDb account.")

        if not os.environ.get("TOOLS_PASS"):
            os.environ["TOOLS_PASS"] = d.get_password(
                "Tools page 'admin' password",
                "Please enter password for tools page 'admin' access.")

        system("echo 'Setting password envars using different passwords ...'")

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
    solrold = os.environ.get("SOLR_OLD")
    if solrold and not solrold == "None":
        system("python %s/bin/initialize/python/solr.py" % formavid)

    # Tools password.
    system("python %s/bin/initialize/python/tools.py" % formavid)

    system("echo 'Finished updating the appliance passwords.'")

    # Make envars available to parent.
    app_pass = os.environ.get["APP_PASS"]
    db_pass = os.environ.get["DB_PASS"]
    solr_new = os.environ.get["SOLR_NEW"]
    print([app_pass, db_pass, solr_new])

if __name__ == "__main__":
    main()

