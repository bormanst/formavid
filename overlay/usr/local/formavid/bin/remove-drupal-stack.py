#!/usr/bin/python
"""Create drupal stack

Option:
    --dbpass=     unless provided, will ask interactively
    --sitename=   unless provided, will ask interactively
    --tld=        unless provided, will ask interactively
    --pass=       unless provided, will ask interactively

"""

import sys
import getopt
import string
import MySQLdb as mdb
import os.path

from dialog_wrapper import Dialog
from executil import system

def usage(s=None):
    if s:
        print >> sys.stderr, "Error:", s
    print >> sys.stderr, "Syntax: %s [options]" % sys.argv[0]
    print >> sys.stderr, __doc__
    sys.exit(1)

def main():
    try:
        opts, args = getopt.gnu_getopt(sys.argv[1:], "dstp",['dbpass=', 'sitename=', 'tld='])
    except getopt.GetoptError, e:
        usage(e)

    dbpass = ""
    sitename = ""
    tld = ""
    for opt, val in opts:
        if opt in ('-d', '--dbpass'):
            dbpass = val
        elif opt in ('-s', '--sitename'):
            sitename = val
        elif opt in ('-t', '--tld'):
            tld = val

    if not tld:
        sitename = ""
        d = Dialog('Drupal Stack Creator - Enter top level doman')
        tld = d.get_input(
            "Enter tld (top level domain) in http://www.sitebasename.TLD",
            "Please enter tld (top level domain) without a dot (e.g. com, org, net).")

    if not sitename:
        d = Dialog('Drupal Stack Creator - Enter site base name')
        sitename = d.get_input(
            "Enter site base name in http://www.SITEBASENAME.%s" % tld,
            "Please enter site base name (without http://www. or .%s)." % tld)

    sitename = sitename.replace(" ","").lower()
    tld = tld.lower()
    hostname = ".".join([sitename,tld])

    # Verify not initial base site.
    apache_conf = ".".join([hostname,'conf'])
    apache_conf = "-".join(['/etc/apache2/sites-available/aaa',apache_conf])
    if os.path.isfile(apache_conf):
        system("echo ''")
        system("echo ''")
        system("echo 'Should not remove initial base site stack for %s...'" % hostname)
        system("echo ''")
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

    if not dbpass:
        d = Dialog("Drupal Stack Creator - MySQL root password REQUIRED!!!")
        dbpass = d.get_password(
            "Restricted - ensure valid appliance backup before running!",
            "Please enter password for the MySQL root account.")
            
    try:
        con = mdb.connect(host="localhost", user="root", passwd="%s" % dbpass)

        # Start stack removal.
        system("echo ''")
        system("echo 'Removing site stack for %s...'" % hostname)
        system("echo ''")

        # Hosts - remove hosts: order important.
        system("echo ''")
        system("echo 'Removing %s entries from hosts...'" % hostname)
        system("echo ''")
        system("sed -i 's/poll.%s\\s//' /etc/hosts" % hostname)
        system("sed -i 's/poll.%s//' /etc/hosts" % hostname)
        system("sed -i 's/forum.%s\\s//' /etc/hosts" % hostname)
        system("sed -i 's/book.%s\\s//' /etc/hosts" % hostname)
        system("sed -i 's/blog.%s\\s//' /etc/hosts" % hostname)
        system("sed -i 's/aggregator.%s\\s//' /etc/hosts" % hostname)
        system("sed -i 's/%s\\s//' /etc/hosts" % hostname)

        # Apache - remove stack conf.
        system("echo ''")
        system("echo 'Removing apache2 confs for %s...'" % hostname)
        system("echo ''")
        system("touch /etc/apache2/sites-enabled/%s.conf" % hostname)
        system("rm -f /etc/apache2/sites-enabled/%s.conf" % hostname)
        system("touch /etc/apache2/sites-available/%s.conf" % hostname)
        system("rm -f /etc/apache2/sites-available/%s.conf" % hostname)
        system("service apache2 restart")

        # Postfix - remove virtual addresses.
        system("echo ''")
        system("echo 'Removing postfix virtual addresses for %s...'" % hostname)
        system("echo ''")
        system("sed -i '/%s/d' /etc/postfix/virtual" % hostname)
        system("postmap /etc/postfix/virtual")
        system("service postfix restart")
 
        # Solr - remove cores.
        system("echo ''")
        system("echo 'Removing solr cores for %s...'" % hostname)
        system("echo ''")
        solrdata = "/var/lib/solr/data"
        system("touch %s/%s" % (solrdata,sitename))
        system("rm -rf %s/%s" % (solrdata,sitename))
        system("service solr restart")

        # Drupal - remove stack sites.
        system("echo ''")
        system("echo 'Removing drupal stack sites for %s...'" % hostname)
        system("echo ''")
        system("touch /var/www/drupal7/sites/poll.%s" % hostname)
        system("rm -rf /var/www/drupal7/sites/poll.%s" % hostname)
        system("touch /var/www/drupal7/sites/forum.%s" % hostname)
        system("rm -rf /var/www/drupal7/sites/forum.%s" % hostname)
        system("touch /var/www/drupal7/sites/book.%s" % hostname)
        system("rm -rf /var/www/drupal7/sites/book.%s" % hostname)
        system("touch /var/www/drupal7/sites/blog.%s" % hostname)
        system("rm -rf /var/www/drupal7/sites/blog.%s" % hostname)
        system("touch /var/www/drupal7/sites/aggregator.%s" % hostname)
        system("rm -rf /var/www/drupal7/sites/aggregator.%s" % hostname)
        system("touch /var/www/drupal7/sites/%s" % hostname)
        system("rm -rf /var/www/drupal7/sites/%s" % hostname)

        # Drupal - remove tools logo symlink.
        system("echo ''")
        system("echo 'Remove logo symlink for %s from tools...'" % hostname)
        system("echo ''")
        if not sitename.lower() == "formavid":
            system("touch /var/www/admin/images/%s.png" % sitename)
            system("rm -f /var/www/admin/images/%s.png" % sitename)

        # Drupal - remove stack site theme.
        system("echo ''")
        system("echo 'Removing drupal theme for %s...'" % hostname)
        system("echo ''")
        system("touch /var/www/drupal7/sites/all/themes/%s" % sitename)
        system("rm -rf /var/www/drupal7/sites/all/themes/%s" % sitename)

        # Clear drupal caches.
        system("drush -r /var/www/drupal7 cc all")

        # Get db cursor.
        cur = con.cursor()

        # MySQL - remove tables.
        system("echo ''")
        system("echo 'Removing mysql databases for %s...'" % hostname)
        system("echo ''")
        cur.execute("DROP DATABASE IF EXISTS %s_aggregator;" % sitename)
        cur.execute("DROP DATABASE IF EXISTS %s_article;" % sitename)
        cur.execute("DROP DATABASE IF EXISTS %s_blog;" % sitename)
        cur.execute("DROP DATABASE IF EXISTS %s_book;" % sitename)
        cur.execute("DROP DATABASE IF EXISTS %s_forum;" % sitename)
        cur.execute("DROP DATABASE IF EXISTS %s_poll;" % sitename)
        cur.execute("FLUSH PRIVILEGES;")

        # Finished removing stack.
        system("echo ''")
        system("echo 'Site stack removal for %s has been completed.'" % hostname)
        system("echo ''")
        system("echo 'Site will no longer be available.'")
        system("echo 'Please verify by trying each site that was in the stack.'")
        system("echo 'It is highly recommended to immediately backup the the appliance again with %s just removed.'" % hostname)
        system("echo ''")

    except mdb.Error, e:
  
        print "Error %d: %s" % (e.args[0],e.args[1])
        sys.exit(1)
    
    finally:    
	
        if con:    
    	    con.close()

if __name__ == "__main__":
    main()
