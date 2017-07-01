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
        opts, args = getopt.gnu_getopt(sys.argv[1:], "dstp",['dbpass=', 'sitename=', 'tld=', 'pass='])
    except getopt.GetoptError, e:
        usage(e)

    dbpass = ""
    sitename = ""
    tld = ""
    password = ""
    for opt, val in opts:
        if opt in ('-d', '--dbpass'):
            dbpass = val
        elif opt in ('-s', '--sitename'):
            sitename = val
        elif opt in ('-t', '--tld'):
            tld = val
        elif opt in ('-p', '--pass'):
            password = val

    if not tld:
        sitename = ""
        d = Dialog('Drupal Stack Creator - Set top level doman')
        tld = d.get_input(
            "Set tld (top level domain) in http://www.sitebasename.TLD",
            "Please enter tld (top level domain) without a dot (e.g. com, org, net).")

    if not sitename:
        d = Dialog('Drupal Stack Creator - Set site base name')
        sitename = d.get_input(
            "Set site base name in http://www.SITEBASENAME.%s" % tld,
            "Please enter site base name (without http://www. or .%s)." % tld)

    sitebasename = sitename 
    sitename = sitename.replace(" ","").lower()
    hostname = ".".join([sitename,tld])
    email = "@".join(['admin',hostname])

    if not dbpass:
        d = Dialog("Drupal Stack Creator - MySQL root password REQUIRED!!!")
        dbpass = d.get_password(
            "Restricted - ensure sufficient resources before running.",
            "Please enter password for the MySQL root account.")
            
    if not password:
        d = Dialog("Drupal Stack Creator - Drupal7 admin password REQUIRED!!!")
        password = d.get_password(
            "Restricted - ensure sufficient resources before running.",
            "Please enter password for the Drupal7 admin account.")

    try:
        con = mdb.connect(host="localhost", user="root", passwd="%s" % dbpass)

        # Sites - templates location.
        templates = "/usr/local/formavid"

        # Sites - ensure clean start.
        system("rm -rf %s/sites-staging" % templates)

        # Sites - set types.
        siteTypes = ['article','aggregator','blog','book','forum','poll']

        # Solr - set core properties.
        system("echo ''")
        system("echo 'Creating and configuring solr search cores.'")
        system("echo ''")
        for sitetype in siteTypes:
            # Solr - no search for aggregator.
            if sitetype != 'aggregator':
                system("mkdir -p %s/%s/%s" % (templates,sitename,sitetype))
                system("cp -f %s/cores-template/core.properties.template %s/%s/%s/core.properties" % (templates,templates,sitename,sitetype))
                system("sed -i \"s/sedsitename/%s/g\" %s/%s/%s/core.properties" % (sitename,templates,sitename,sitetype))
                system("sed -i \"s/sedsitetype/%s/g\" %s/%s/%s/core.properties" % (sitetype,templates,sitename,sitetype))

        # Solr - load cores.
        solrdata = "/var/lib/solr/data"
        system("mv %s/%s %s" % (templates,sitename,solrdata))

        # Solr - copy drupal solr conf.
        apachesolr = "/var/www/drupal7/sites/all/modules/apachesolr/solr-conf/solr-4.x"
        for sitetype in siteTypes:
            # Solr - no search for aggregator.
            if sitetype != 'aggregator':
                system("cp -r %s %s/%s/%s/conf" % (apachesolr,solrdata,sitename,sitetype))

        # Solr - ensure owner.
        system("chown -R solr:solr %s/%s" % (solrdata,sitename))

        # Solr - enable changes.
        system("service solr restart")
        system("echo ''")
        system("echo 'Solr search cores have been created.'")
        system("echo ''")

        # Hosts - update.
        for sitetype in siteTypes:
            sitetypemod = ''
            if sitetype != 'article':
                sitetypemod = sitetype + '.'
            system("sed -i '/127.0.1.1/s/$/ %s%s/' /etc/hosts" % (sitetypemod,hostname))

        # Sites - prepare templates.
        system("cp -rf %s/sites-template %s/sites-staging" % (templates,templates))

        # Apache - replace sitehostname in confs.
        system("find %s/sites-staging -name \"*.conf\" -exec sed -i \"s/sitehostname/%s/g\" '{}' \\;" % (templates,hostname))

        # Apache - add sites available.
        system("cp -f %s/sites-staging/sitehostname.conf /etc/apache2/sites-available/%s.conf" % (templates,hostname))

        # Apache - enable added sites.
        system("cp -sf /etc/apache2/sites-available/%s.conf /etc/apache2/sites-enabled/." % hostname)

        # Start initial stack setup.
        system("echo ''")
        system("echo 'Creating site stack for %s - this takes a while...'" % hostname)
        system("echo ''")

        # Create drupal sites.
        for sitetype in siteTypes:
            sitetypemod = ''
            sitetypetitle = ''
            if sitetype != 'article':
                sitetypemod = sitetype + '.'
                sitetypetitle = ' ' + sitetype.title() + 's'
            # Create site type.
            system("echo 'Creating site: %s%s'" % (sitetypemod,hostname))
            system("cp -f /var/www/drupal7/sites/default/stack.settings.php /var/www/drupal7/sites/default/settings.php")
            system("chown www-data:www-data /var/www/drupal7/sites/default/settings.php")
            system("drush -q -r /var/www/drupal7 site-install standard -y --account-name=admin --account-pass=%s --db-su=root --db-su-pw=%s --db-url=mysql://admin:%s@localhost/%s_%s --site-name=\"%s%s\" --account-mail=admin@%s --site-mail=admin@%s --sites-subdir=%s%s" % (password,dbpass,password,sitename,sitetype,sitebasename,sitetypetitle,hostname,hostname,sitetypemod,hostname))
            system("sed -i \"s/# \\$cookie_domain = '.example.com'\;/\\$cookie_domain = '.%s'\;/g\" /var/www/drupal7/sites/%s/settings.php" % (hostname,hostname))
            # Sites - update permissions.
            system("chown root:www-data /var/www/drupal7/sites/%s%s/settings.php" % (sitetypemod,hostname))
            system("chmod 640 /var/www/drupal7/sites/%s%s/settings.php" % (sitetypemod,hostname))
            system("chown -R www-data:www-data /var/www/drupal7/sites/%s%s/files" % (sitetypemod,hostname))
            system("chmod 777 /var/www/drupal7/sites/%s%s/files" % (sitetypemod,hostname))

        # Sites - clean up.
        system("cp -f /var/www/drupal7/sites/default/stack.settings.php /var/www/drupal7/sites/default/settings.php")
        system("chown root:www-data /var/www/drupal7/sites/default/settings.php")
        system("chmod 640 /var/www/drupal7/sites/default/settings.php")
        system("rm -rf %s/sites-staging" % templates)

        # Get db cursor.
        cur = con.cursor()

        # Sites - set additional database properties.
        for sitetype in siteTypes:
            # Allow perms for drush.
            cur.execute("GRANT ALL PRIVILEGES ON %s_%s.* TO drupal7@localhost WITH GRANT OPTION;" % (sitename,sitetype))
            # Update admin email attributes.
            cur.execute('UPDATE %s_%s.users SET mail=\"admin@%s\" WHERE name=\"admin\";' % (sitename,sitetype,hostname))
            cur.execute('UPDATE %s_%s.users SET init=\"admin@%s\" WHERE name=\"admin\";' % (sitename,sitetype,hostname))

        # Finish initial stack setup.
        system("echo ''")
        system("echo 'Site stack for %s has been created.'" % hostname)
        system("echo ''")

        # Restart services.
        system("echo ''")
        system("echo 'Restarting apache2 to activate %s site stack.'" % hostname)
        system("echo ''")
        system("service apache2 restart")
        system("echo ''")
        system("echo 'Site stack for %s is now available to configure.'" % hostname)
        system("echo ''")

        # Clear drupal caches.
        system("echo ''")
        system("echo 'Clear drupal caches.'")
        system("echo ''")
        system("drush -r /var/www/drupal7 cc all")

        # Start configuring stack.
        system("echo ''")
        system("echo 'Configuring site stack for %s - this takes a while...'" % hostname)
        system("echo ''")

        # Drupal - create site theme from zen sub-theme.
        system("drush -r /var/www/drupal7 --uri=http://%s zen \"%s\"" % (hostname,sitename))

        # Drupal - set site theme cssadmin access.
        system("chown -R cssadmin:cssadmin /var/www/drupal7/sites/all/themes/%s" % (sitename))
        system("chmod -R 775 /var/www/drupal7/sites/all/themes/%s" % (sitename))

        # Drupal - enable/disable properties.
        for sitetype in siteTypes:
            sitetypemod = ''
            if sitetype != 'article':
                sitetypemod = sitetype + '.'
            # Start configuring sites.
            system("echo ''")
            system("echo ''")
            system("echo 'Enabling and disabling Drupal properties for %s%s ...'" % (sitetypemod,hostname))
            system("echo ''")
            # Enable site theme.
            system("drush -r /var/www/drupal7 --uri=http://%s%s pm-enable --yes '%s'" % (sitetypemod,hostname,sitename))
            # Set default theme.
            system("drush -r /var/www/drupal7 --uri=http://%s%s vset --yes theme_default '%s'" % (sitetypemod,hostname,sitename))
            # Enable solr modules. No search for aggregator.
            if sitetype != 'aggregator':
                system("drush -r /var/www/drupal7 --uri=http://%s%s pm-enable apachesolr --yes" % (sitetypemod,hostname))
                system("drush -r /var/www/drupal7 --uri=http://%s%s pm-enable apachesolr_access --yes" % (sitetypemod,hostname))
                system("drush -r /var/www/drupal7 --uri=http://%s%s pm-enable apachesolr_search --yes" % (sitetypemod,hostname))
                system("drush -r /var/www/drupal7 --uri=http://%s%s solr-set-env-url http://drupal7:%s@localhost:8983/solr/%s.%s" % (sitetypemod,hostname,password,sitename,sitetype))
                system("drush -r /var/www/drupal7 --uri=http://%s%s vset --yes search_default_module 'apachesolr_search'" % (sitetypemod,hostname))
            # Enable site specific.
            if sitetype != 'article':
                system("drush -r /var/www/drupal7 --uri=http://%s.%s pm-enable --yes %s" % (sitetype,hostname,sitetype))
            # Enable contact form.
            system("drush -r /var/www/drupal7 --uri=http://%s%s pm-enable --yes contact" % (sitetypemod,hostname))
            # Disable overlay.
            system("drush -r /var/www/drupal7 --uri=http://%s%s pm-disable --yes overlay" % (sitetypemod,hostname))
            # Disable dashboard.
            system("drush -r /var/www/drupal7 --uri=http://%s%s pm-disable --yes dashboard" % (sitetypemod,hostname))
            # Disable footer block.
            system("mysql -u root --password=%s -e \"UPDATE %s_%s.block SET status=0 WHERE module='system' AND delta='powered-by' AND theme='%s'\"" % (dbpass,sitename,sitetype,sitename))

        # Symlink logo to admin page.
        system("chmod -R 644 /var/www/drupal7/sites/all/themes/%s/logo.png" % (sitename))
        if not sitename.lower() == "formavid":
            system("ln -s /var/www/drupal7/sites/all/themes/%s/logo.png /var/www/admin/images/%s.png" % (sitename,sitename))

        # Finished configuring stack.
        system("echo ''")
        system("echo ''")
        system("echo 'Site stack for %s has been configured.'" % hostname)
        system("echo ''")
        system("echo 'All of the sites should be available immediately.'")
        system("echo 'Please verify the stack by visiting the drupal status report for each site.'")
        system("echo ''")
        system("echo ''")

        # Postfix virtual addresses.
        system("echo ''")
        system("echo 'Adding %s email addresses to postfix.'" % hostname)
        system("echo ''")
        system("echo 'webmaster@%s admin' >> /etc/postfix/virtual" % hostname)
        system("echo 'admin@%s admin' >> /etc/postfix/virtual" % hostname)
        system("echo 'support@%s admin' >> /etc/postfix/virtual" % hostname)
        system("service postfix start")
        system("postmap /etc/postfix/virtual")
        system("service postfix stop")
        system("echo ''")
        system("echo 'Postfix has been updated.'")
        system("echo ''")

        # Clear drupal caches.
        system("echo ''")
        system("echo 'Clear drupal caches.'")
        system("echo ''")
        system("drush -r /var/www/drupal7 cc all")
        system("echo ''")

    except mdb.Error, e:
  
        print "Error %d: %s" % (e.args[0],e.args[1])
        sys.exit(1)
    
    finally:    
	
        if con:    
    	    con.close()

if __name__ == "__main__":
    main()
