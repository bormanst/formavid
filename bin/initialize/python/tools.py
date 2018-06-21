#!/usr/bin/python
# Copyright (C) 2018 Sean Borman <bormanst@gmail.com>.
# You should have received LICENSE.txt, a copy of the
# GNU General Public License, along with this program.
# If not, see <https://www.gnu.org/licenses/>.

"""

Set tools password

Option:
    --pass=     unless provided, will ask interactively

"""

import os

from dialog_wrapper import Dialog
from local_methods import *

DEFAULT_DIALOG_HEADER = "FormaVid - First boot configuration"

def main():
    username = "admin"
    password = os.environ.get("TOOLS_PASS")

    d = Dialog(DEFAULT_DIALOG_HEADER)

    if not password:
        password = d.get_password(
            "Tools page admin Password",
            "Please enter password for tools page admin access.")

    # apache2 htdbm password
    directory = "/usr/local/apache2/passwd/admintools"
    if not os.path.isdir(directory): system("mkdir -p %s" % directory)
    directory = "".join([directory, '/passwords.dbm'])
    command = " ".join(['htdbm -bc', directory, username, password])
    system(command)

    # set webmin root password
    system("/usr/share/webmin/changepass.pl /etc/webmin root %s" % password)

    # restart apache2
    system('systemctl restart apache2')

if __name__ == "__main__":
    main()

