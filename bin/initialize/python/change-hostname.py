#!/usr/bin/python
# Copyright (C) 2018 Sean Borman <bormanst@gmail.com>.
# You should have received LICENSE.txt, a copy of the
# GNU General Public License, along with this program.
# If not, see <https://www.gnu.org/licenses/>.

"""

Change hostname for appliance.

"""

import fnmatch
import os
import string

from dialog_wrapper import Dialog
from local_methods import *

DEFAULT_DIALOG_HEADER = "FormaVid - First boot configuration"
DEFAULT_DOMAIN = "www.examplesitename.com"
DEFAULT_TITLE = "Example Site Name"

def main():
    # Check default apache admin conf.
    old_file = "/etc/apache2/sites-available/zzz-admin.%s.conf" % default_sitename
    if not os.path.exists(old_file):
        system("echo ''")
        system("echo 'The default hostname has already been updated.'")
        system("echo ''")
        quit()

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
    # Set admin email.
    app_email = '@'.join(["admin", hostname])

    # Update system files.
    system("echo 'Updating FormaVid default envars ...'")
    old_file = "/etc/formavid/default_envars"
    system("sed -i 's/%s/%s/g' %s" % (default_domain, domain, old_file))
    system("sed -i 's/%s/%s/g' %s" % (default_sitetitle, sitetitle, old_file))
    old_file = "/etc/hosts"
    system("sed -i 's/%s/%s/g' %s" % (default_hostname, hostname, old_file))

    # Update admin tools.
    system("echo 'Updating FormaVid admin pages and tools ...'")
    system("a2dissite %s" % old_file)
    system("sed -i 's/%s/%s/g' %s" % (default_hostname, hostname, old_file))
    new_file = "/etc/apache2/sites-available/zzz-admin.%s.conf" % sitename
    system("mv %s %s" % (old_file, new_file))
    system("a2ensite %s" % new_file)
    old_file = "/var/www/admin/*.php"
    system("sed -i 's/%s/%s/g' %s" % (default_sitename, sitename, old_file))
    system("sed -i 's/%s/%s/g' %s" % (default_sitetitle, sitetitle, old_file))
    system("sed -i 's/%s/%s/g' %s" % (default_hostname, hostname, old_file))

    # Update apache2 files.
    system("echo 'Updating Apache2 status.conf file ...'")
    old_file = "/etc/apache2/mods-available/status.conf"
    system("sed -i 's/%s/%s/g' %s" % (default_sitename, sitename, old_file))
    system("sed -i 's/%s/%s/g' %s" % (default_sitetitle, sitetitle, old_file))

    # Update invoiceninja files.
    system("echo 'Updating Imvoice Ninja apache.conf file ...'")
    old_file = "/etc/invoiceninja/apache.conf"
    system("sed -i 's/%s/%s/g' %s" % (default_hostname, hostname, old_file))
    old_file = "/var/www/invoiceninja/.env"
    system("sed -i 's/%s/%s/g' %s" % (default_hostname, hostname, old_file))

    # Update postfix files.
    system("echo 'Updating Postfix virtual file ...'")
    old_file = "/etc/postfix/virtual"
    system("sed -i 's/%s/%s/g' %s" % (default_hostname, hostname, old_file))
    system("postconf -e myhostname=%s" % hostname)
    system("postconf -e smtpd_banner='$myhostname ESMTP'")

    # Update roundup files.
    system("echo 'Updating Roundup support tracker apache.conf file ...'")
    old_file = "/etc/roundup/support/apache.conf"
    system("sed -i 's/%s/%s/g' %s" % (default_hostname, hostname, old_file))
    old_file = "/etc/roundup/support/tracker-config.ini"
    system("sed -i 's/%s/%s/g' %s" % (default_sitetitle, sitetitle, old_file))
    system("sed -i 's/%s/%s/g' %s" % (default_hostname, hostname, old_file))

    # Make envars available to parent.
    print([domain, sitetitle, app_email])

if __name__ == "__main__":
    main()

