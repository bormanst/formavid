#!/usr/bin/python
# Copyright (C) 2018 Sean Borman <bormanst@gmail.com>.
# You should have received LICENSE.txt, a copy of the
# GNU General Public License, along with this program.
# If not, see <https://www.gnu.org/licenses/>.

"""

Perform GCE initialization to update passwords and domain info.

"""

import os
import string

from local_methods import *

DEFAULT_SINGLE_PASSWORD="F0rm4V1d"

def main():
    # Check blocked.
    blocking_file = "/etc/formavid/do_not_delete_this_file"
    sites = "/var/www/drupal8/prod/web/sites/sites.php"
    if os.path.exists(blocking_file) or os.path.exists(sites):
        system("echo ''")
        system("echo 'The gce-initialization script is blocked from executing.'")
        system("echo ''")
        quit()

    # Get random password.
    alphabet = string.ascii_letters + string.digits
    single_pass = ''.join(choice(alphabet) for i in range(16))

    # Set envars.
    os.environ["APP_PASS"] = ""
    os.environ["DB_PASS"] = ""
    os.environ["DOMAIN"] = ""
    os.environ["INVOICENINJA_PASS"] = ""
    os.environ["ROUNDUP_PASS"] = ""
    os.environ["SINGLE_PASS"] = single_pass
    os.environ["SITETITLE"] = ""
    os.environ["SOLR_NEW"] = ""
    os.environ["SOLR_OLD"] = DEFAULT_SINGLE_PASSWORD
    os.environ["SYNC_CSSADMIN"] = "True"
    os.environ["TOOLS_PASS"] = ""
    os.environ["WEBMIN_PASS"] = ""

    # set dir containing init scripts
    scripts_dir = "/usr/local/formavid/bin"

    # wipe default passwords with random as security precaution
    script = "/".join([scripts_dir, "initialize/python/change-passwords.py"])
    system(script)

    # set old solr password to just created random
    os.environ["SOLR_OLD"] = single_pass

    # wipe random password
    os.environ["SINGLE_PASS"] = ""

    # update appliance with user selected values
    script = "/".join([scripts_dir, "initialize/python/change-hostname.py"])
    system(script)
    script = "/".join([scripts_dir, "initialize/python/change-passwords.py"])
    system(script)

    # create initial stack
    script = "/".join([scripts_dir, "deploy/python/create-drupal-stack.py"])
    system(script)

    # regen ssh keys
    script = "/".join([scripts_dir, "initialize/shell/regen_sshkeys"])
    system(script)

    # re-initialize etckeeper
    script = "/".join([scripts_dir, "initialize/shell/init_etckeeper"])
    system(script)

    # create blocking file
    system('echo "The absence of this file causes the GCE start-up script to reset hostname and passwords." > %s' % blocking_file)
    system('chmod 0444 %s' % blocking_file)

if __name__ == "__main__":
    main()
