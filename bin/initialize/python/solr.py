#!/usr/bin/python
# Copyright (C) 2018 Sean Borman <bormanst@gmail.com>.
# You should have received LICENSE.txt, a copy of the
# GNU General Public License, along with this program.
# If not, see <https://www.gnu.org/licenses/>.

"""

Set solr password

"""

import os
from local_methods import *

def main():
    # Get envars.
    adminpass = os.environ.get("APP_PASS")

    # Solr - finish password protection.
    # TODO: use curl method.

if __name__ == "__main__":
    main()

