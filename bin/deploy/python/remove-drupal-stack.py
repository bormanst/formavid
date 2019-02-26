#!/usr/bin/python
# Copyright (C) 2018 Sean Borman <bormanst@gmail.com>.
# You should have received LICENSE.txt, a copy of the
# GNU General Public License, along with this program.
# If not, see <https://www.gnu.org/licenses/>.

"""

Remove drupal stack

Option:
    --dbpass=     unless provided, will ask interactively
    --domain=   unless provided, will ask interactively

"""

import datetime
import getopt
import logging
import MySQLdb as mdb
import os
import string
import sys

from dialog_wrapper import Dialog
from local_methods import *

DEFAULT_DIALOG_HEADER = "Formavid - Drupal site removal script"
DEFAULT_DOMAIN = "example.com"
DEFAULT_LOG = "/var/log/formavid/remove-druapl-stack.log"

def usage(s=None):
    if s:
        print >> sys.stderr, "Error:", s
    print >> sys.stderr, "Syntax: %s [options]" % sys.argv[0]
    print >> sys.stderr, __doc__
    sys.exit(1)

def main():
    try:
        opts, args = getopt.gnu_getopt(sys.argv[1:], "dstp",['dbpass=', 'domain='])
    except getopt.GetoptError, e:
        usage(e)

    # log setup
    logging.basicConfig(filename=DEFAULT_LOG,level=logging.INFO)

    # log start
    logging.info('Start time: %s' % datetime.datetime.now())

    # Initialize vars.
    dbpass = ""
    domain = ""

    # Assign common dialog header.
    d = Dialog(DEFAULT_DIALOG_HEADER)

    # Check inputs.
    for opt, val in opts:
        if opt in ('-d', '--dbpass'):
            dbpass = val
        elif opt in ('-s', '--domain'):
            domain = val

    # check for dbpass
    isdbpass = "DbpasswordProvided"
    if not dbpass or dbpass == "None": isdbpass = "No-DbpasswordProvided"

    # log envars
    logging.info('Incoming opts: [isdbpass]:[domain]')
    logging.info('Incoming opts: [%s]:[%s]' % (isdbpass, domain))

    # Check domain.
    if not (domain):
        domain = d.get_input(
            "Delete Drupal8 stack for a domain",
            "Enter the domain to delete from the stack.",
            DEFAULT_DOMAIN)

    # Preen domain.
    domain = format_domain(domain)

    # Get hostname.
    hostname = get_hostname(domain)

    # Get sitename.
    sitename = get_sitename(domain)

    # Verify not initial base site.
    apache_conf = ".".join([hostname,'conf'])
    apache_conf = "-".join(['/etc/apache2/sites-available/aaa', apache_conf])
    if os.path.isfile(apache_conf):
        system("echo ''")
        system("echo ''")
        system("echo 'Should not remove initial base site stack for %s ...'" % hostname)
        system("echo ''")
        system("echo 'Manually remove the prefix \"aaa-\" file %s and rerun this script if you really must remove the initial stack completely.'" % apache_conf)
        system("echo ''")
        system("echo 'Be aware that the /etc/hostname entry and some tools will still reference %s and should be updated accordingly.'" % hostname)
        system("echo ''")
        system("echo 'After completing all modifications, remember to manually prefix \"aaa-\" to only one STACK.conf file at /etc/apache2/[sites-avaialble,sites-enabled(symlink)] so that it precedes all other apache sites.'")
        system("echo ''")
        system("echo 'Ensure a valid appliance backup exists before running!!!'")
        system("echo ''")
        sys.exit(1)

    # Check dbpass.
    if not dbpass:
        dbpass = d.get_password(
            "Restricted - ensure valid appliance backup before running!",
            "Please enter password for the MySQL root account.")

    # log vars
    logging.info('Vars used to remove stack: [isdbpass]:[domain]:[hostname]:[sitename]')
    logging.info('Vars used to remove stack: [%s]:[%s]:[%s]:[%s]' % (isdbpass, domain, hostname, sitename))

    # log create start
    logging.info('Starting stack removal: %s' % datetime.datetime.now())

    # Start stack removal.
    system("echo ''")
    system("echo 'Removing site stack for %s ...'" % hostname)
    system("echo ''")

    # Hosts - remove hosts: order important.
    system("echo ''")
    system("echo 'Removing %s entries from hosts ...'" % hostname)
    system("echo ''")
    system("sed -i 's/poll.%s\\s//' /etc/hosts" % hostname)
    system("sed -i 's/poll.%s//' /etc/hosts" % hostname)
    system("sed -i 's/forum.%s\\s//' /etc/hosts" % hostname)
    system("sed -i 's/book.%s\\s//' /etc/hosts" % hostname)
    system("sed -i 's/blog.%s\\s//' /etc/hosts" % hostname)
    system("sed -i 's/aggregator.%s\\s//' /etc/hosts" % hostname)
    system("sed -i 's/%s\\s//' /etc/hosts" % hostname)
    # log info
    logging.info('/etc/hosts removals complete.')

    # Apache - remove stack conf.
    system("echo ''")
    system("echo 'Removing apache2 confs for %s ...'" % hostname)
    system("echo ''")
    system("touch /etc/apache2/sites-enabled/%s.conf" % hostname)
    system("rm -f /etc/apache2/sites-enabled/%s.conf" % hostname)
    system("touch /etc/apache2/sites-available/%s.conf" % hostname)
    system("rm -f /etc/apache2/sites-available/%s.conf" % hostname)
    system("systemctl restart apache2")
    # log info
    logging.info('Apache2 conf removals complete.')

    # Postfix - remove virtual addresses.
    system("echo ''")
    system("echo 'Removing postfix virtual addresses for %s ...'" % hostname)
    system("echo ''")
    system("sed -i '/%s/d' /etc/postfix/virtual" % hostname)
    system("postmap /etc/postfix/virtual")
    system("systemctl restart postfix")
    # log info
    logging.info('Postfix removals complete.')

    # Solr - remove cores.
    solrdata = "/var/lib/solr/data"
    if os.path.exists(solrdata):
        system("echo ''")
        system("echo 'Removing solr cores for %s ...'" % hostname)
        system("echo ''")
        system("touch %s/%s" % (solrdata, sitename))
        system("rm -rf %s/%s" % (solrdata, sitename))
        # Check solr service running.
        out = system("systemctl is-active solr")
        if out.strip().lower() == 'active':
            # Restart to apply changes.
            system("systemctl restart solr")
        # log info
        logging.info('Solr removals complete.')

    # TODO: Add option to specify subdir
    drupalsubdir = "prod"

    # Sites - drupal loaction.
    drupaldir = "/".join(["/var/www/drupal8",drupalsubdir,"web"])

    # Drupal - remove stack sites.
    sites = "/".join([drupaldir,"sites"])
    if os.path.exists(sites):
        system("echo ''")
        system("echo 'Removing drupal stack sites for %s ...'" % hostname)
        system("echo ''")
        system("touch %s/poll.%s" % (sites, hostname))
        system("rm -rf %s/poll.%s" % (sites, hostname))
        system("sed -i '/poll.%s/d' %s/sites.php" % (hostname, sites))
        system("touch %s/forum.%s" % (sites, hostname))
        system("rm -rf %s/forum.%s" % (sites, hostname))
        system("sed -i '/forum.%s/d' %s/sites.php" % (hostname, sites))
        system("touch %s/book.%s" % (sites, hostname))
        system("rm -rf %s/book.%s" % (sites, hostname))
        system("sed -i '/book.%s/d' %s/sites.php" % (hostname, sites))
        system("touch %s/blog.%s" % (sites, hostname))
        system("rm -rf %s/blog.%s" % (sites, hostname))
        system("sed -i '/blog.%s/d' %s/sites.php" % (hostname, sites))
        system("touch %s/aggregator.%s" % (sites, hostname))
        system("rm -rf %s/aggregator.%s" % (sites, hostname))
        system("sed -i '/aggregator.%s/d' %s/sites.php" % (hostname, sites))
        system("touch %s/%s" % (sites, hostname))
        system("rm -rf %s/%s" % (sites, hostname))
        system("sed -i '/%s/d' %s/sites.php" % (hostname, sites))
        # log info
        logging.info('Drupal directory removals complete.')

    # Drupal - remove tools logo symlink.
    system("echo ''")
    system("echo 'Remove logo symlink for %s from tools ...'" % hostname)
    system("echo ''")
    if not sitename == "formavidorg":
        system("touch /var/www/admin/images/%s.svg" % sitename)
        system("rm -f /var/www/admin/images/%s.svg" % sitename)
        # log info
        logging.info('Removed logo symlink for %s from tools ...' % hostname)

    # Drupal - remove stack site theme.
    theme = "/".join([drupaldir,"themes",sitename])
    if os.path.exists(theme):
        system("echo ''")
        system("echo 'Removing drupal theme for %s ...'" % hostname)
        system("echo ''")
        system("rm -rf %s" % theme)
        # log info
        logging.info('Removed drupal theme for %s.' % hostname)

    # Drupal - remove site theme from git repo.
    theme = "/".join(["/var/lib/git/drupal8",drupalsubdir,"web/themes",sitename])
    if os.path.exists(theme):
        system("echo ''")
        system("echo 'Removing git repo for %s theme ...'" % hostname)
        system("echo ''")
        system("rm -rf %s" % theme)
        # log info
        logging.info('Removed git repo for %s theme.' % hostname)

    try:
        # Get db cursor.
        con = mdb.connect(host="localhost", user="root", passwd="%s" % dbpass)
        cur = con.cursor()
        # MySQL - remove tables.
        system("echo ''")
        system("echo 'Removing mysql databases for %s ...'" % hostname)
        system("echo ''")
        cur.execute("DROP DATABASE IF EXISTS %s_aggregator;" % sitename)
        cur.execute("DROP DATABASE IF EXISTS %s_article;" % sitename)
        cur.execute("DROP DATABASE IF EXISTS %s_blog;" % sitename)
        cur.execute("DROP DATABASE IF EXISTS %s_book;" % sitename)
        cur.execute("DROP DATABASE IF EXISTS %s_forum;" % sitename)
        cur.execute("DROP DATABASE IF EXISTS %s_poll;" % sitename)
        cur.execute("FLUSH PRIVILEGES;")
        # log info
        logging.info('Removed mysql databases for %s.' % hostname)
    except mdb.Error, e:
        print "Error %d: %s" % (e.args[0],e.args[1])
        # log info
        logging.info('Error Removing mysql databases for %s.' % hostname)
        sys.exit(1)
    finally:
        if con:
            con.close()

    # Apache - remove stack conf.
    system("systemctl restart apache2")
    logging.info('Restarted apache2 after removals completed.')

    # Finished removing stack.
    system("echo ''")
    system("echo 'Site stack removal for %s has been completed.'" % hostname)
    system("echo ''")
    system("echo 'Site will no longer be available.'")
    system("echo 'Please verify by trying each site that was in the stack.'")
    system("echo 'It is highly recommended to immediately backup the the appliance again with %s just removed.'" % hostname)
    system("echo ''")

    # log end
    logging.info('Completed stack removal for %s: %s' % (hostname, datetime.datetime.now()))

if __name__ == "__main__":
    main()
