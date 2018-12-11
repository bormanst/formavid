#!/usr/bin/python
# Copyright (C) 2018 Sean Borman <bormanst@gmail.com>.
# You should have received LICENSE.txt, a copy of the
# GNU General Public License, along with this program.
# If not, see <https://www.gnu.org/licenses/>.

"""

Change hostname for appliance.

"""

import os
import string

from dialog_wrapper import Dialog
from local_methods import *

DEFAULT_DIALOG_HEADER = "FormaVid - First boot configuration"
DEFAULT_DOMAIN = "www.examplesitename.com"
DEFAULT_TITLE = "Example Site Name"

def main():
    # Assign common dialog header.
    d = Dialog(DEFAULT_DIALOG_HEADER)

    # Set envars.
    default_domain = format_domain(DEFAULT_DOMAIN)
    default_hostname = get_hostname(default_domain)
    default_sitename = get_sitename(default_domain)
    default_sitetitle = DEFAULT_TITLE

    # Get domain.
    domain = d.get_input(
        "Set Base Appliance Domain",
        "Please enter the domain to be used for this appliance.",
        DEFAULT_DOMAIN)

    # Get site title.
    sitetitle = d.get_input(
        "Set Base Appliance Site Title",
        "Please enter the site title to be used for this appliance.",
        DEFAULT_TITLE)

    # Format domain.
    domain = format_domain(domain)
    # Get hostname.
    hostname = get_hostname(domain)
    # Get sitename.
    sitename = get_sitename(domain)

    # Update system files.
    old_file = "/etc/formavid/default_envars"
    system("sed -i 's/%s/%s/g' %s" % (default_domain, domain, old_file))
    system("sed -i 's/%s/%s/g' %s" % (default_sitetitle, sitetitle, old_file))
    old_file = "/etc/hosts"
    system("sed -i 's/%s/%s/g' %s" % (default_hostname, hostname, old_file))

    # Update admin tools.
    new_file = "/etc/apache2/sites-available/zzz-admin.%s.conf" % sitename
    old_file = "/etc/apache2/sites-available/zzz-admin.%s.conf" % default_sitename
    system("sed -i 's/%s/%s/g' %s" % (default_hostname, hostname, old_file))
    system("mv %s %s" % (old_file, new_file))
    old_file = "/var/www/admin/*.php"
    system("sed -i 's/%s/%s/g' %s" % (default_sitename, sitename, old_file))
    system("sed -i 's/%s/%s/g' %s" % (default_sitetitle, sitetitle, old_file))
    system("sed -i 's/%s/%s/g' %s" % (default_hostname, hostname, old_file))

    # Update apache2 files.
    old_file = "/etc/apache2/mods-available/status.conf"
    system("sed -i 's/%s/%s/g' %s" % (default_sitename, sitename, old_file))
    system("sed -i 's/%s/%s/g' %s" % (default_sitetitle, sitetitle, old_file))

    # Update invoiceninja files.
    old_file = "/etc/invoiceninja/apache.conf"
    system("sed -i 's/%s/%s/g' %s" % (default_hostname, hostname, old_file))
    old_file = "/var/www/invoiceninja/.env"
    system("sed -i 's/%s/%s/g' %s" % (default_hostname, hostname, old_file))

    # Update postfix files.
    old_file = "/etc/postfix/virtual"
    system("sed -i 's/%s/%s/g' %s" % (default_hostname, hostname, old_file))
    system("postconf -e myhostname=%s" % hostname)
    system("postconf -e smtpd_banner='$myhostname ESMTP'")

    # Update roundup files.
    old_file = "/etc/roundup/support/apache.conf"
    system("sed -i 's/%s/%s/g' %s" % (default_hostname, hostname, old_file))
    old_file = "/etc/roundup/support/tracker-config.ini"
    system("sed -i 's/%s/%s/g' %s" % (default_sitetitle, sitetitle, old_file))
    system("sed -i 's/%s/%s/g' %s" % (default_hostname, hostname, old_file))

if __name__ == "__main__":
    main()