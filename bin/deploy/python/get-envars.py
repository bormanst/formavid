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

ENVARS_TEXT = """This sets custom variables such as domain, emails, and passwords.

Warning!!! It is a major security risk to use defaults. Minimally, reset passwords before moving to production.

Run formavid/bin/initialize_appliance script to reset only the passwords.

Site build defaults are located formavid/bin/deploy/shell/default_envars."""

DEFAULT_DIALOG_HEADER = "FormaVid - First boot configuration"
DEFAULT_DOMAIN = "www.examplesitename.com"
DEFAULT_TITLE = "Example Site Name"

def main():
    # Initialize vars.
    user_defined = True
    reset_passwords_only = False

    # Assign common dialog header.
    d = Dialog(DEFAULT_DIALOG_HEADER)

    # Check PASSWORDS_ONLY.
    if "PASSWORDS_ONLY" in os.environ: reset_passwords_only = True

    # Check method for envars.
    if not reset_passwords_only:
        user_defined = d.yesno(
            "Select method to set custom appliance variables:",
            ENVARS_TEXT,
            "User defined",
            "Load defaults")

    # Set envars.
    if user_defined:
        # Check reset passwords only.
        if not reset_passwords_only:
            # Get site domain.
            domain = d.get_input(
                "Drupal8 Site Domain",
                "Enter domain for new Drupal8 site.",
                DEFAULT_DOMAIN)
            domain = format_domain(domain)
            os.environ["DOMAIN"] = domain
            os.environ["APP_HOSTNAME"] = get_hostname(domain)
            os.environ["SITENAME"] = get_sitename(domain)

            # Get site title.
            os.environ["SITETITLE"] = d.get_input(
                "Enter Drupal8 Site Title",
                "Enter title for new Drupal8 site.",
                DEFAULT_TITLE)

            # Get admin email.
            os.environ["APP_EMAIL"] = d.get_email(
                "Appliance admin Email",
                "Please enter email address for the Appliance admin account.",
                "admin@%s" % get_hostname(domain))

            # Check certbot install.
            os.environ["CERTBOT_INSTALL"] = d.yesno(
                "Do you wish to run certbot?",
                "It can be run independently if desired.",
                "No",
                "Yes")

            # Check borgbackup GCS_PROJECT_ID.
            os.environ["GCS_PROJECT_ID"] = d.get_input(
                "Enter GCS Poject ID (not name or number) to automatically create nearline bucket for initial borgbackup.",
                "Entering 'None' will prompt for existing bucket or postpone borgbackup configuration.",
                os.environ.get("GCS_PROJECT_ID"))

            # Check borgbackup GCS_BUCKET.
            if os.environ.get("GCS_PROJECT_ID") == "None":
                os.environ["GCS_BUCKET"] = d.get_input(
                    "Enter GCS bucket name, 'gcs-bucket-name', for initial borgbackup.",
                    "Use 'None' to postpone borgbackup configure.",
                    os.environ.get("GCS_BUCKET"))

        # Set envars for passwords.
        os.environ["APP_PASS"] = d.get_password(
            "Drupal/Solr admin and cssadmin password",
            "Please enter password for Drupal/Solr admin and cssadmin accounts.")

        os.environ["BORGBACKUP_OLD"] = d.get_password(
            "Borgbackup repository existing password",
            "Please enter existing password for the Borgbackup repository.")

        os.environ["BORGBACKUP_PASS"] = d.get_password(
            "Borgbackup repository new password",
            "Please enter new password for the Borgbackup repository.")

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
    else:
        # Use defaults.
        system("%s/bin/deploy/shell/default_envars" % os.environ.get("FORMAVID"))

if __name__ == "__main__":
    main()
