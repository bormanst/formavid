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

        # Solr - no search for aggregator.

        # Solr - set core properties.
        sitetype = "article"
        system("mkdir -p %s/%s/%s" % (templates,sitename,sitetype))
        system("cp -f %s/cores-template/core.properties.template %s/%s/%s/core.properties" % (templates,templates,sitename,sitetype))
        system("sed -i \"s/sedsitename/%s/g\" %s/%s/%s/core.properties" % (sitename,templates,sitename,sitetype))
        system("sed -i \"s/sedsitetype/%s/g\" %s/%s/%s/core.properties" % (sitetype,templates,sitename,sitetype))

        sitetype = "blog"
        system("mkdir -p %s/%s/%s" % (templates,sitename,sitetype))
        system("cp -f %s/cores-template/core.properties.template %s/%s/%s/core.properties" % (templates,templates,sitename,sitetype))
        system("sed -i \"s/sedsitename/%s/g\" %s/%s/%s/core.properties" % (sitename,templates,sitename,sitetype))
        system("sed -i \"s/sedsitetype/%s/g\" %s/%s/%s/core.properties" % (sitetype,templates,sitename,sitetype))

        sitetype = "book"
        system("mkdir -p %s/%s/%s" % (templates,sitename,sitetype))
        system("cp -f %s/cores-template/core.properties.template %s/%s/%s/core.properties" % (templates,templates,sitename,sitetype))
        system("sed -i \"s/sedsitename/%s/g\" %s/%s/%s/core.properties" % (sitename,templates,sitename,sitetype))
        system("sed -i \"s/sedsitetype/%s/g\" %s/%s/%s/core.properties" % (sitetype,templates,sitename,sitetype))

        sitetype = "forum"
        system("mkdir -p %s/%s/%s" % (templates,sitename,sitetype))
        system("cp -f %s/cores-template/core.properties.template %s/%s/%s/core.properties" % (templates,templates,sitename,sitetype))
        system("sed -i \"s/sedsitename/%s/g\" %s/%s/%s/core.properties" % (sitename,templates,sitename,sitetype))
        system("sed -i \"s/sedsitetype/%s/g\" %s/%s/%s/core.properties" % (sitetype,templates,sitename,sitetype))

        sitetype = "poll"
        system("mkdir -p %s/%s/%s" % (templates,sitename,sitetype))
        system("cp -f %s/cores-template/core.properties.template %s/%s/%s/core.properties" % (templates,templates,sitename,sitetype))
        system("sed -i \"s/sedsitename/%s/g\" %s/%s/%s/core.properties" % (sitename,templates,sitename,sitetype))
        system("sed -i \"s/sedsitetype/%s/g\" %s/%s/%s/core.properties" % (sitetype,templates,sitename,sitetype))

        # Solr - load cores.
        solrdata = "/var/lib/solr/data"
        system("mv %s/%s %s" % (templates,sitename,solrdata))

        # Solr - copy drupal solr conf.
        apachesolr = "/var/www/drupal7/sites/all/modules/apachesolr/solr-conf/solr-4.x"
        system("cp -r %s %s/%s/article/conf" % (apachesolr,solrdata,sitename))
        system("cp -r %s %s/%s/blog/conf" % (apachesolr,solrdata,sitename))
        system("cp -r %s %s/%s/book/conf" % (apachesolr,solrdata,sitename))
        system("cp -r %s %s/%s/forum/conf" % (apachesolr,solrdata,sitename))
        system("cp -r %s %s/%s/poll/conf" % (apachesolr,solrdata,sitename))

        # Solr - ensure owner.
        system("chown -R solr:solr %s/%s" % (solrdata,sitename))

        # Solr - enable changes.
        system("service solr restart")

        # Hosts - add to hosts as needed.
        system("sed -i '/127.0.1.1/s/$/ %s/' /etc/hosts" % hostname)
        system("sed -i '/127.0.1.1/s/$/ aggregator.%s/' /etc/hosts" % hostname)
        system("sed -i '/127.0.1.1/s/$/ blog.%s/' /etc/hosts" % hostname)
        system("sed -i '/127.0.1.1/s/$/ book.%s/' /etc/hosts" % hostname)
        system("sed -i '/127.0.1.1/s/$/ forum.%s/' /etc/hosts" % hostname)
        system("sed -i '/127.0.1.1/s/$/ poll.%s/' /etc/hosts" % hostname)

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
        system("echo 'Creating site: %s'" % hostname)
        system("cp -f /var/www/drupal7/sites/default/stack.settings.php /var/www/drupal7/sites/default/settings.php")
        system("drush -q -r /var/www/drupal7 site-install standard -y --account-name=admin --account-pass=%s --db-su=root --db-su-pw=%s --db-url=mysql://admin:%s@localhost/%s_article --site-name=\"%s\" --account-mail=admin@%s --site-mail=admin@%s --sites-subdir=%s" % (password,dbpass,password,sitename,sitebasename,hostname,hostname,hostname))
        system("sed -i \"s/# \\$cookie_domain = '.example.com'\;/\\$cookie_domain = '.%s'\;/g\" /var/www/drupal7/sites/%s/settings.php" % (hostname,hostname))

        system("echo 'Creating site: aggregator.%s'" % hostname)
        system("cp -f /var/www/drupal7/sites/default/stack.settings.php /var/www/drupal7/sites/default/settings.php")
        system("drush -q -r /var/www/drupal7 site-install standard -y --account-name=admin --account-pass=%s --db-su=root --db-su-pw=%s --db-url=mysql://admin:%s@localhost/%s_aggregator --site-name=\"%s Aggregator\" --account-mail=admin@%s --site-mail=admin@%s --sites-subdir=aggregator.%s" % (password,dbpass,password,sitename,sitebasename,hostname,hostname,hostname))
        system("sed -i \"s/# \\$cookie_domain = '.example.com'\;/\\$cookie_domain = '.%s'\;/g\" /var/www/drupal7/sites/aggregator.%s/settings.php" % (hostname,hostname))

        system("echo 'Creating site: blog.%s'" % hostname)
        system("cp -f /var/www/drupal7/sites/default/stack.settings.php /var/www/drupal7/sites/default/settings.php")
        system("drush -q -r /var/www/drupal7 site-install standard -y --account-name=admin --account-pass=%s --db-su=root --db-su-pw=%s --db-url=mysql://admin:%s@localhost/%s_blog --site-name=\"%s Blogs\" --account-mail=admin@%s --site-mail=admin@%s --sites-subdir=blog.%s" % (password,dbpass,password,sitename,sitebasename,hostname,hostname,hostname))
        system("sed -i \"s/# \\$cookie_domain = '.example.com'\;/\\$cookie_domain = '.%s'\;/g\" /var/www/drupal7/sites/blog.%s/settings.php" % (hostname,hostname))

        system("echo 'Creating site: book.%s'" % hostname)
        system("cp -f /var/www/drupal7/sites/default/stack.settings.php /var/www/drupal7/sites/default/settings.php")
        system("drush -q -r /var/www/drupal7 site-install standard -y --account-name=admin --account-pass=%s --db-su=root --db-su-pw=%s --db-url=mysql://admin:%s@localhost/%s_book --site-name=\"%s Manuals\" --account-mail=admin@%s --site-mail=admin@%s --sites-subdir=book.%s" % (password,dbpass,password,sitename,sitebasename,hostname,hostname,hostname))
        system("sed -i \"s/# \\$cookie_domain = '.example.com'\;/\\$cookie_domain = '.%s'\;/g\" /var/www/drupal7/sites/book.%s/settings.php" % (hostname,hostname))

        system("echo 'Creating site: forum.%s'" % hostname)
        system("cp -f /var/www/drupal7/sites/default/stack.settings.php /var/www/drupal7/sites/default/settings.php")
        system("drush -q -r /var/www/drupal7 site-install standard -y --account-name=admin --account-pass=%s --db-su=root --db-su-pw=%s --db-url=mysql://admin:%s@localhost/%s_forum --site-name=\"%s Forums\" --account-mail=admin@%s --site-mail=admin@%s --sites-subdir=forum.%s" % (password,dbpass,password,sitename,sitebasename,hostname,hostname,hostname))
        system("sed -i \"s/# \\$cookie_domain = '.example.com'\;/\\$cookie_domain = '.%s'\;/g\" /var/www/drupal7/sites/forum.%s/settings.php" % (hostname,hostname))

        system("echo 'Creating site: poll.%s'" % hostname)
        system("cp -f /var/www/drupal7/sites/default/stack.settings.php /var/www/drupal7/sites/default/settings.php")
        system("drush -q -r /var/www/drupal7 site-install standard -y --account-name=admin --account-pass=%s --db-su=root --db-su-pw=%s --db-url=mysql://admin:%s@localhost/%s_poll --site-name=\"%s Polls\" --account-mail=admin@%s --site-mail=admin@%s --sites-subdir=poll.%s" % (password,dbpass,password,sitename,sitebasename,hostname,hostname,hostname))
        system("sed -i \"s/# \\$cookie_domain = '.example.com'\;/\\$cookie_domain = '.%s'\;/g\" /var/www/drupal7/sites/poll.%s/settings.php" % (hostname,hostname))

        system("cp -f /var/www/drupal7/sites/default/stack.settings.php /var/www/drupal7/sites/default/settings.php")

        # Sites - clean up.
        system("rm -rf %s/sites-staging" % templates)

        # Get db cursor.
        cur = con.cursor()

        # Sites - add admin user for drush.
        cur.execute("GRANT ALL PRIVILEGES ON %s_aggregator.* TO drupal7@localhost WITH GRANT OPTION;" % sitename)
        cur.execute("GRANT ALL PRIVILEGES ON %s_article.* TO drupal7@localhost WITH GRANT OPTION;" % sitename)
        cur.execute("GRANT ALL PRIVILEGES ON %s_blog.* TO drupal7@localhost WITH GRANT OPTION;" % sitename)
        cur.execute("GRANT ALL PRIVILEGES ON %s_book.* TO drupal7@localhost WITH GRANT OPTION;" % sitename)
        cur.execute("GRANT ALL PRIVILEGES ON %s_forum.* TO drupal7@localhost WITH GRANT OPTION;" % sitename)
        cur.execute("GRANT ALL PRIVILEGES ON %s_poll.* TO drupal7@localhost WITH GRANT OPTION;" % sitename)

        # Sites - set file permissions.
        system("chmod 777 /var/www/drupal7/sites/%s/files" % hostname)
        system("chmod 777 /var/www/drupal7/sites/aggregator.%s/files" % hostname)
        system("chmod 777 /var/www/drupal7/sites/blog.%s/files" % hostname)
        system("chmod 777 /var/www/drupal7/sites/book.%s/files" % hostname)
        system("chmod 777 /var/www/drupal7/sites/forum.%s/files" % hostname)
        system("chmod 777 /var/www/drupal7/sites/poll.%s/files" % hostname)

        # Finish initial stack setup.
        system("echo ''")
        system("echo 'Site stack for %s has been created.'" % hostname)
        system("echo ''")

        # Restart services.
        system("service apache2 restart")

        # Clear drupal caches.
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

        # Drupal - enable site theme.
        system("drush -r /var/www/drupal7 --uri=http://%s pm-enable --yes '%s'" % (hostname,sitename))
        system("drush -r /var/www/drupal7 --uri=http://aggregator.%s pm-enable --yes '%s'" % (hostname,sitename))
        system("drush -r /var/www/drupal7 --uri=http://blog.%s pm-enable --yes '%s'" % (hostname,sitename))
        system("drush -r /var/www/drupal7 --uri=http://book.%s pm-enable --yes '%s'" % (hostname,sitename))
        system("drush -r /var/www/drupal7 --uri=http://forum.%s pm-enable --yes '%s'" % (hostname,sitename))
        system("drush -r /var/www/drupal7 --uri=http://poll.%s pm-enable --yes '%s'" % (hostname,sitename))

        # Drupal - set default theme.
        system("drush -r /var/www/drupal7 --uri=http://%s vset --yes theme_default '%s'" % (hostname,sitename))
        system("drush -r /var/www/drupal7 --uri=http://aggregator.%s vset --yes theme_default '%s'" % (hostname,sitename))
        system("drush -r /var/www/drupal7 --uri=http://blog.%s vset --yes theme_default '%s'" % (hostname,sitename))
        system("drush -r /var/www/drupal7 --uri=http://book.%s vset --yes theme_default '%s'" % (hostname,sitename))
        system("drush -r /var/www/drupal7 --uri=http://forum.%s vset --yes theme_default '%s'" % (hostname,sitename))
        system("drush -r /var/www/drupal7 --uri=http://poll.%s vset --yes theme_default '%s'" % (hostname,sitename))

        # Enable solr modules.
        # No search for aggregator.
        system("drush -r /var/www/drupal7 --uri=http://%s pm-enable apachesolr --yes" % (hostname))
        system("drush -r /var/www/drupal7 --uri=http://blog.%s pm-enable apachesolr --yes" % (hostname))
        system("drush -r /var/www/drupal7 --uri=http://book.%s pm-enable apachesolr --yes" % (hostname))
        system("drush -r /var/www/drupal7 --uri=http://forum.%s pm-enable apachesolr --yes" % (hostname))
        system("drush -r /var/www/drupal7 --uri=http://poll.%s pm-enable apachesolr --yes" % (hostname))

        system("drush -r /var/www/drupal7 --uri=http://%s pm-enable apachesolr_access --yes" % (hostname))
        system("drush -r /var/www/drupal7 --uri=http://blog.%s pm-enable apachesolr_access --yes" % (hostname))
        system("drush -r /var/www/drupal7 --uri=http://book.%s pm-enable apachesolr_access --yes" % (hostname))
        system("drush -r /var/www/drupal7 --uri=http://forum.%s pm-enable apachesolr_access --yes" % (hostname))
        system("drush -r /var/www/drupal7 --uri=http://poll.%s pm-enable apachesolr_access --yes" % (hostname))

        system("drush -r /var/www/drupal7 --uri=http://%s pm-enable apachesolr_search --yes" % (hostname))
        system("drush -r /var/www/drupal7 --uri=http://blog.%s pm-enable apachesolr_search --yes" % (hostname))
        system("drush -r /var/www/drupal7 --uri=http://book.%s pm-enable apachesolr_search --yes" % (hostname))
        system("drush -r /var/www/drupal7 --uri=http://forum.%s pm-enable apachesolr_search --yes" % (hostname))
        system("drush -r /var/www/drupal7 --uri=http://poll.%s pm-enable apachesolr_search --yes" % (hostname))

        # Update solr urls.
        # No search for aggregator.
        system("drush -r /var/www/drupal7 --uri=http://%s solr-set-env-url http://drupal7:%s@localhost:8983/solr/%s.article" % (hostname,password,sitename))
        system("drush -r /var/www/drupal7 --uri=http://blog.%s solr-set-env-url http://drupal7:%s@localhost:8983/solr/%s.blog" % (hostname,password,sitename))
        system("drush -r /var/www/drupal7 --uri=http://book.%s solr-set-env-url http://drupal7:%s@localhost:8983/solr/%s.book" % (hostname,password,sitename))
        system("drush -r /var/www/drupal7 --uri=http://forum.%s solr-set-env-url http://drupal7:%s@localhost:8983/solr/%s.forum" % (hostname,password,sitename))
        system("drush -r /var/www/drupal7 --uri=http://poll.%s solr-set-env-url http://drupal7:%s@localhost:8983/solr/%s.poll" % (hostname,password,sitename))

        # Drupal - set solr as default search.
        system("drush -r /var/www/drupal7 --uri=http://%s vset --yes search_default_module 'apachesolr_search'" % (hostname))
        system("drush -r /var/www/drupal7 --uri=http://blog.%s vset --yes search_default_module 'apachesolr_search'" % (hostname))
        system("drush -r /var/www/drupal7 --uri=http://book.%s vset --yes search_default_module 'apachesolr_search'" % (hostname))
        system("drush -r /var/www/drupal7 --uri=http://forum.%s vset --yes search_default_module 'apachesolr_search'" % (hostname))
        system("drush -r /var/www/drupal7 --uri=http://poll.%s vset --yes search_default_module 'apachesolr_search'" % (hostname))

        # Enable site specific.
        system("drush -r /var/www/drupal7 --uri=http://aggregator.%s pm-enable --yes aggregator" % (hostname))
        system("drush -r /var/www/drupal7 --uri=http://blog.%s pm-enable --yes blog" % (hostname))
        system("drush -r /var/www/drupal7 --uri=http://book.%s pm-enable --yes book" % (hostname))
        system("drush -r /var/www/drupal7 --uri=http://forum.%s pm-enable --yes forum" % (hostname))
        system("drush -r /var/www/drupal7 --uri=http://poll.%s pm-enable --yes poll" % (hostname))

        # Enable contact form.
        system("drush -r /var/www/drupal7 --uri=http://%s pm-enable --yes contact" % (hostname))
        system("drush -r /var/www/drupal7 --uri=http://aggregator.%s pm-enable --yes contact" % (hostname))
        system("drush -r /var/www/drupal7 --uri=http://blog.%s pm-enable --yes contact" % (hostname))
        system("drush -r /var/www/drupal7 --uri=http://book.%s pm-enable --yes contact" % (hostname))
        system("drush -r /var/www/drupal7 --uri=http://forum.%s pm-enable --yes contact" % (hostname))
        system("drush -r /var/www/drupal7 --uri=http://poll.%s pm-enable --yes contact" % (hostname))

        # Disable overlay.
        system("drush -r /var/www/drupal7 --uri=http://%s pm-disable --yes overlay" % (hostname))
        system("drush -r /var/www/drupal7 --uri=http://aggregator.%s pm-disable --yes overlay" % (hostname))
        system("drush -r /var/www/drupal7 --uri=http://blog.%s pm-disable --yes overlay" % (hostname))
        system("drush -r /var/www/drupal7 --uri=http://book.%s pm-disable --yes overlay" % (hostname))
        system("drush -r /var/www/drupal7 --uri=http://forum.%s pm-disable --yes overlay" % (hostname))
        system("drush -r /var/www/drupal7 --uri=http://poll.%s pm-disable --yes overlay" % (hostname))

        # Disable dashboard.
        system("drush -r /var/www/drupal7 --uri=http://%s pm-disable --yes dashboard" % (hostname))
        system("drush -r /var/www/drupal7 --uri=http://aggregator.%s pm-disable --yes dashboard" % (hostname))
        system("drush -r /var/www/drupal7 --uri=http://blog.%s pm-disable --yes dashboard" % (hostname))
        system("drush -r /var/www/drupal7 --uri=http://book.%s pm-disable --yes dashboard" % (hostname))
        system("drush -r /var/www/drupal7 --uri=http://forum.%s pm-disable --yes dashboard" % (hostname))
        system("drush -r /var/www/drupal7 --uri=http://poll.%s pm-disable --yes dashboard" % (hostname))

        # Sites - disable footer block.
        system("mysql -u root --password=%s -e \"UPDATE %s_article.block SET status=0 WHERE module='system' AND delta='powered-by' AND theme='%s'\"" % (dbpass,sitename,sitename))
        system("mysql -u root --password=%s -e \"UPDATE %s_aggregator.block SET status=0 WHERE module='system' AND delta='powered-by' AND theme='%s'\"" % (dbpass,sitename,sitename))
        system("mysql -u root --password=%s -e \"UPDATE %s_blog.block SET status=0 WHERE module='system' AND delta='powered-by' AND theme='%s'\"" % (dbpass,sitename,sitename))
        system("mysql -u root --password=%s -e \"UPDATE %s_book.block SET status=0 WHERE module='system' AND delta='powered-by' AND theme='%s'\"" % (dbpass,sitename,sitename))
        system("mysql -u root --password=%s -e \"UPDATE %s_forum.block SET status=0 WHERE module='system' AND delta='powered-by' AND theme='%s'\"" % (dbpass,sitename,sitename))
        system("mysql -u root --password=%s -e \"UPDATE %s_poll.block SET status=0 WHERE module='system' AND delta='powered-by' AND theme='%s'\"" % (dbpass,sitename,sitename))

        # Symlink logo to admin page.
        system("chmod -R 644 /var/www/drupal7/sites/all/themes/%s/logo.png" % (sitename))
        if not sitename.lower() == "formavid":
            system("ln -s /var/www/drupal7/sites/all/themes/%s/logo.png /var/www/admin/images/%s.png" % (sitename,sitename))

        # Finished configuring stack.
        system("echo ''")
        system("echo 'Site stack for %s has been configured.'" % hostname)
        system("echo ''")
        system("echo 'All of the sites should be available immediately.'")
        system("echo 'Please verify the stack by visiting the status report for each site.'")
        system("echo ''")

        # Clear drupal caches.
        system("drush -r /var/www/drupal7 cc all")

        # Postfix virtual addresses.
        system("echo 'webmaster@%s admin' >> /etc/postfix/virtual" % hostname)
        system("echo 'admin@%s admin' >> /etc/postfix/virtual" % hostname)
        system("echo 'support@%s admin' >> /etc/postfix/virtual" % hostname)
        system("service postfix start")
        system("postmap /etc/postfix/virtual")
        system("service postfix stop")

    except mdb.Error, e:
  
        print "Error %d: %s" % (e.args[0],e.args[1])
        sys.exit(1)
    
    finally:    
	
        if con:    
    	    con.close()

if __name__ == "__main__":
    main()
