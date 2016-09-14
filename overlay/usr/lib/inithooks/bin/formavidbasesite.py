#!/usr/bin/python
"""Set base site

Option:
    --apass=   unless provided, will ask interactively
    --basesitename= unless provided, will ask interactively
    --email= unless provided, will ask interactively
    --hostname= unless provided, will ask interactively

"""

import sys
import getopt
import string

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
        opts, args = getopt.gnu_getopt(sys.argv[1:], "abeh", ['apass=','email=','hostname=','sitename='])
    except getopt.GetoptError, e:
        usage(e)

    adminpass = ""
    sitename = ""
    email = ""
    hostname = ""

    for opt, val in opts:
        if opt in ('-a', '--apass'):
            adminpass = val
        elif opt in ('-e', '--email'):
            email = val
        elif opt in ('-p', '--hostname'):
            hostname = val
        elif  opt in ('-b', '--sitename'):
            sitename = val

    lowername = sitename.replace(" ","").lower()

    # Hostname entry.
    system("echo %s > /etc/hostname" % hostname)
    system("/etc/init.d/hostname.sh start")
    system("sed -i \"s/sedhostname/%s/g\" /etc/confconsole/services.txt" % hostname)

    # Remove formavid from hosts.
    system("sed -i 's/ formavid//g' /etc/hosts")

    # Apache admin email.
    system("sed -i 's/webmaster@localhost/%s/g' /etc/adminer/apache.conf" % email)
    system("sed -i 's/webmaster@localhost/%s/g' /etc/roundup/apache.conf" % email)
    system("sed -i 's/webmaster@localhost/%s/g' /etc/simpleinvoices/apache.conf" % email)
      
    # Roundup.
    system("sed -i '/127.0.1.1/s/$/ support.%s/' /etc/hosts" % hostname)
    system("find /etc/roundup -name \"apache.conf\" -exec sed -i \"s/sedlowername/%s/g\" '{}' \\;" % lowername)
    system("find /etc/roundup -name \"apache.conf\" -exec sed -i \"s/sedhostname/%s/g\" '{}' \\;" % hostname)
    system("find /etc/roundup -name \"tracker-config.ini\" -exec sed -i \"s/web = \//web = https:\/\/support.%s\/support\//g\" '{}' \\;" % hostname)
    system("find /etc/roundup -name \"tracker-config.ini\" -exec sed -i \"s/domain = example.com/domain = %s/g\" '{}' \\;" % hostname)
    system("cp -sf /etc/roundup/apache.conf /etc/apache2/sites-available/zzz-support.%s.conf" % hostname)
    system("cp -sf /etc/apache2/sites-available/zzz-support.%s.conf /etc/apache2/sites-enabled/." % hostname)
    system("rm -f /etc/apache2/sites-available/roundup")
    system("rm -f /etc/apache2/sites-enabled/roundup")

    # Simple Invoices.
    system("sed -i '/127.0.1.1/s/$/ billing.%s/' /etc/hosts" % hostname)
    system("find /etc/simpleinvoices -name \"apache.conf\" -exec sed -i \"s/sedlowername/%s/g\" '{}' \\;" % lowername)
    system("find /etc/simpleinvoices -name \"apache.conf\" -exec sed -i \"s/sedhostname/%s/g\" '{}' \\;" % hostname)
    system("cp -sf /etc/simpleinvoices/apache.conf /etc/apache2/sites-available/zzz-billing.%s.conf" % hostname)
    system("cp -sf /etc/apache2/sites-available/zzz-billing.%s.conf /etc/apache2/sites-enabled/." % hostname)

    # Tools.
    system("sed -i '/127.0.1.1/s/$/ admin.%s/' /etc/hosts" % hostname)
    system("sed -i 's/sedlowername/%s/g' /var/www/admin/*.php" % lowername)
    system("sed -i 's/sedsitename/%s/g' /var/www/admin/*.php" % sitename)
    system("sed -i 's/sedhostname/%s/g' /var/www/admin/*.php" % hostname)
    system("cp -f /usr/local/formavid/admin-template/zzz-admin.sitehostname.conf /etc/apache2/sites-available/zzz-admin.%s.conf" % hostname)
    system("find /etc/apache2/sites-available -name \"zzz-admin.%s.conf\" -exec sed -i \"s/sedlowername/%s/g\" '{}' \\;" % (hostname,lowername))
    system("find /etc/apache2/sites-available -name \"zzz-admin.%s.conf\" -exec sed -i \"s/sedhostname/%s/g\" '{}' \\;" % (hostname,hostname))
    system("cp -sf /etc/apache2/sites-available/zzz-admin.%s.conf /etc/apache2/sites-enabled/." % hostname)

    # Postfix.
    system("touch /etc/postfix/virtual")
    system("echo 'support: admin' >> /etc/aliases")
    system("echo 'webmaster@localhost admin' >> /etc/postfix/virtual")
    system("echo 'root@%s admin' >> /etc/postfix/virtual" % hostname)
    system("service postfix start")
    system("newaliases")
    system("postmap /etc/postfix/virtual")
    system("postconf -e 'virtual_alias_maps = hash:/etc/postfix/virtual'")
    system("postconf -e 'smtpd_tls_CAfile = /etc/ssl/certs/cacert.org.pem'")
    system("postfix reload")

    # Drupal -  redirect default install.php to base site.
    system("mv -f /usr/local/src/install.php /var/www/drupal7/install.php")
    system("sed -i 's/sedhostname/%s/g' /var/www/drupal7/install.php" % hostname)

    # NOTE: Link other themes to base theme after stack created above for theme folder to exist.

    # Update header input.
    system("sed -i 's/sedsitename/%s/g' /usr/local/src/header.txt" % sitename)
 
    # Update title input.
    system("sed -i 's/sedsitename/%s/g' /usr/local/src/title.txt" % sitename)

    # Simple Invoices theme.
    system("sed -i '/<title/d' /var/www/simpleinvoices/templates/default/header.tpl")
    system("sed -i '/favicon.ico/d' /var/www/simpleinvoices/templates/default/header.tpl")
    system("sed -i '/<head/r /usr/local/src/styles.txt' /var/www/simpleinvoices/templates/default/header.tpl")
    system("sed -i 's/<style>/<!-- <style>/' /var/www/simpleinvoices/templates/default/header.tpl")
    system("sed -i 's/<\/style>/<\/style> -->/' /var/www/simpleinvoices/templates/default/header.tpl")
    system("sed -i '/<head/r /usr/local/src/title.txt' /var/www/simpleinvoices/templates/default/header.tpl")
    system("sed -i '/<body/r /usr/local/src/header.txt' /var/www/simpleinvoices/templates/default/header.tpl")
    system("sed -i 's/sedtoolname/Billing/g' /var/www/simpleinvoices/templates/default/header.tpl")
    system("rm -f /var/www/simpleinvoices/tmp/cache/*")

    # Roundup theme.
    system("sed -i '/<title/d' /var/www/support/html/page.html")
    system("sed -i '/<head/r /usr/local/src/styles.txt' /var/www/support/html/page.html")
    system("sed -i '/<head/r /usr/local/src/title.txt' /var/www/support/html/page.html")
    system("sed -i '/<body/r /usr/local/src/header.txt' /var/www/support/html/page.html")
    system("sed -i 's/sedtoolname/Support/g' /var/www/support/html/page.html")
    system("sed -i 's|/theme/|/support/theme/|g' /var/www/support/html/page.html")
    system("sed -i 's|href=\"/\"|href=\"/support/\"|g' /var/www/support/html/page.html")

    # Admin theme - leave title alone.
    system("sed -i '/<head/r /usr/local/src/styles.txt' /var/www/admin/*.php")
    system("sed -i '/<body/r /usr/local/src/header.txt' /var/www/admin/*.php")
    system("sed -i 's/sedtoolname/Admin/g' /var/www/admin/*.php")

    # Apache theme.
    system("sed -i 's/sedsitename/%s/g' /usr/local/src/status.conf" % sitename)
    system("mv -f /usr/local/src/status.conf /etc/apache2/mods-available")

    # Clean up.
    system("rm /usr/local/src/header.txt")
    system("rm /usr/local/src/styles.txt")
    system("rm /usr/local/src/title.txt")

    # TKLBAM create initial custom backup profile.
    system("tklbam-internal create-profile /usr/local/formavid/tklbam/formavid.conf/ /usr/local/formavid/tklbam/profile.conf")

if __name__ == "__main__":
    main()
    
