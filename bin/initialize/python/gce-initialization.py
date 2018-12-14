#!/usr/bin/python
# Copyright (C) 2018 Sean Borman <bormanst@gmail.com>.
# You should have received LICENSE.txt, a copy of the
# GNU General Public License, along with this program.
# If not, see <https://www.gnu.org/licenses/>.

"""

Perform GCE initialization to update passwords and domain info.

"""

import ast
import os
import string
import subprocess

from local_methods import *

DEFAULT_SINGLE_PASSWORD="F0rm4V1d"

def gen_password(length=16, charset="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"):
    random_bytes = os.urandom(length)
    len_charset = len(charset)
    indices = [int(len_charset * (ord(byte) / 256.0)) for byte in random_bytes]
    return "".join([charset[index] for index in indices])

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
    single_pass = gen_password()

    # Set envars.
    os.environ["APP_EMAIL"] = ""
    os.environ["APP_PASS"] = ""
    os.environ["DB_PASS"] = ""
    os.environ["DOMAIN"] = ""
    os.environ["FORMAVID"] = "/usr/local/formavid"
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
    output = subprocess.check_output(script)
    subvals = ast.literal_eval(output.decode("ascii"))
    if subvals[0]: os.environ["DOMAIN"] = subvals[0]
    if subvals[1]: os.environ["SITETITLE"] = subvals[1]
    if subvals[2]: os.environ["APP_EMAIL"] = subvals[2]

    script = "/".join([scripts_dir, "initialize/python/change-passwords.py"])
    output = subprocess.check_output(script)
    subvals = ast.literal_eval(output.decode("ascii"))
    if subvals[0]: os.environ["APP_PASS"] = subvals[0]
    if subvals[1]: os.environ["DB_PASS"] = subvals[1]
    if subvals[2]: os.environ["SOLR_NEW"] = subvals[2]

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
