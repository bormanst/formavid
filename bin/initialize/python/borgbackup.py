#!/usr/bin/python
# Copyright (C) 2018 Sean Borman <bormanst@gmail.com>.
# You should have received LICENSE.txt, a copy of the
# GNU General Public License, along with this program.
# If not, see <https://www.gnu.org/licenses/>.

"""

Set Borgbackup admin password and email

"""

import hashlib
import os
import MySQLdb as mdb

from dialog_wrapper import Dialog
from local_methods import *

DEFAULT_DIALOG_HEADER = "FormaVid - First boot configuration"

def main():
    bucket = os.environ.get("GCS_BUCKET")
    old = os.environ.get("BORGBACKUP_OLD")
    password = os.environ.get("BORGBACKUP_PASS")

    d = Dialog(DEFAULT_DIALOG_HEADER)

    if not bucket:
        bucket = d.get_input(
            "Borgbackup repository gcs-bucket-name (not sub-directory)",
            "Please enter gcs-bucket-name for the Borgbackup repository.")

    if not old:
        old = d.get_password(
            "Borgbackup repository CURRENT password",
            "Please enter current password for the Borgbackup repository.")

    if not password:
        password = d.get_password(
            "Borgbackup repository NEW password",
            "Please enter new password for the Borgbackup repository.")

    # mount fuse to BACKUP_DIR
    system("gcsfuse --only-dir borgbackup/ %s /mnt/borgbackup" % bucket)

    # change repository passphrase
    system("BORG_PASSPHRASE=%s BORG_NEW_PASSPHRASE=%s borg key change-passphrase /mnt/borgbackup" % (old, password))

    # unmount fuse
    system("fusermount -u -z /mnt/borgbackup")

if __name__ == "__main__":
    main()

