#!/usr/bin/python
# Copyright (C) 2018 Sean Borman <bormanst@gmail.com>.
# You should have received LICENSE.txt, a copy of the
# GNU General Public License, along with this program.
# If not, see <https://www.gnu.org/licenses/>.

"""

Set Webmin password

"""

import os

from dialog_wrapper import Dialog
from local_methods import *

DEFAULT_DIALOG_HEADER = "FormaVid - First boot configuration"

def main():
    # Get envars.
    password = os.environ.get("WEBMIN_PASS")

    # set vars
    d = Dialog(DEFAULT_DIALOG_HEADER)
    username = "root"

    if not password:
        password = d.get_password(
            "Webmin root password",
            "Please enter password for Webmin root access.")

    # set webmin root password
    system("/usr/share/webmin/changepass.pl /etc/webmin %s %s" % (username, password))

if __name__ == "__main__":
    main()
