#!/usr/bin/python
# Copyright (C) 2018 Sean Borman <bormanst@gmail.com>.
# You should have received LICENSE.txt, a copy of the
# GNU General Public License, along with this program.
# If not, see <https://www.gnu.org/licenses/>.

"""

Reboot to install kernel upgrade

"""

import getopt
import signal
import sys

from dialog_wrapper import Dialog

TEXT = """A security update to the kernel requires a reboot to go into effect.

For maximum protection, we recommend rebooting now.
"""

def usage(s=None):
    if s:
        print >> sys.stderr, "Error:", s
    print >> sys.stderr, "Syntax: %s [options]" % sys.argv[0]
    print >> sys.stderr, __doc__
    sys.exit(1)

class ExecError(Exception):
    """Accessible attributes:
    command executed command
    exitcode    non-zero exitcode returned by command
    output  error output returned by command
    """
    def __init__(self, command, exitcode, output=None):
        Exception.__init__(self, command, exitcode, output)

        self.command = command
        self.exitcode = exitcode
        self.output = output

    def __str__(self):
        str = "non-zero exitcode (%d) for command: %s" % (self.exitcode,
                                                          self.command)
        if self.output:
            str += "\n" + self.output
        return str

def main():
    signal.signal(signal.SIGINT, signal.SIG_IGN)
    try:
        opts, args = getopt.gnu_getopt(sys.argv[1:], "h", ['help'])
    except getopt.GetoptError, e:
        usage(e)

    for opt, val in opts:
        if opt in ('-h', '--help'):
            usage()

    d = Dialog("FormaVid - Reboot after kernel update")
    reboot  = d.yesno("Reboot now?", TEXT, "Reboot", "Skip")

    if not reboot:
        sys.exit(1)

if __name__ == "__main__":
    main()

