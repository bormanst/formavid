#!/usr/bin/python
# Copyright (C) 2018 Sean Borman <bormanst@gmail.com>.
# You should have received LICENSE.txt, a copy of the
# GNU General Public License, along with this program.
# If not, see <https://www.gnu.org/licenses/>.

"""

Get envars needed for build.

"""

import os
import string

from dialog_wrapper import Dialog
from local_methods import *

ENVARS_TEXT = """This sets passwords.

Warning!!! It is a major security risk to use defaults. Minimally, reset passwords before moving to production.

This script uses the site build defaults located in formavid/bin/deploy/shell/default_envars."""

DEFAULT_DIALOG_HEADER = "FormaVid - First boot configuration"
DEFAULT_DOMAIN = "www.examplesitename.com"
DEFAULT_TITLE = "Example Site Name"

def main():
    # Initialize vars.
    user_defined = True
    reset_passwords_only = False

    # Get envars.
    formavid = "/usr/local/formavid"
    if "FORMAVID" in os.environ: formavid = os.environ.get("FORMAVID")

    # Assign common dialog header.
    d = Dialog(DEFAULT_DIALOG_HEADER)

    # Set envars for passwords.
    os.environ["APP_PASS"] = d.get_password(
        "Drupal admin and cssadmin password",
        "Please enter password for Drupal admin and cssadmin accounts.")

    os.environ["DB_PASS"] = d.get_password(
        "MySQL password",
        "Please enter new password for the MySQL 'root' account.")

    os.environ["ROUNDUP_PASS"] = d.get_password(
        "Roundup admin password",
        "Please enter password for the Roundup admin account.")

    os.environ["SIMPLEINVOICES_PASS"] = d.get_password(
        "Simple Invoices admin password",
        "Enter password for the Simple Invoices apache site access and admin account.")

    os.environ["TOOLS_PASS"] = d.get_password(
        "Tools page admin password",
        "Please enter password for tools page admin access.")

    # MariaDB password.
    system("python %s/bin/initialize/python/mysqlconf.py" % formavid)

    # Drupal password.
    system("python %s/bin/initialize/python/drupal8.py" % formavid)

    # Roundup password.
    system("python %s/bin/initialize/python/roundup.py" % formavid)

    # Simple Invoices password.
    system("python %s/bin/initialize/python/simpleinvoices.py" % formavid)

    # Tools password.
    system("python %s/bin/initialize/python/tools.py" % formavid)

if __name__ == "__main__":
    main()
