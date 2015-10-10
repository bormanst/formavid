#!/usr/bin/python
"""Set hostname

Option:
    --apass=   unless provided, will ask interactively
    --basesitename= unless provided, will ask interactively
    --dbpass= unless provided, will ask interactively
    --email= unless provided, will ask interactively
    --pass= unless provided, will ask interactively
    --rpass= unless provided, will ask interactively
    --sipass= unless provided, will ask interactively
    --tld= unless provided, will ask interactively
    --user= unless provided, will ask interactively
    --zpass= unless provided, will ask interactively

"""

import getopt
import pwd
import string
import sys

from dialog_wrapper import Dialog
from executil import system
from mysqlconf import MySQL

def usage(s=None):
    if s:
        print >> sys.stderr, "Error:", s
    print >> sys.stderr, "Syntax: %s [options]" % sys.argv[0]
    print >> sys.stderr, __doc__
    sys.exit(1)

def main():
    try:
        opts, args = getopt.gnu_getopt(sys.argv[1:], "abdeprstuz", ['apass=','basesitename=','dbpass=','email=','pass=','rpass=','sipass=','tld=','user=','zpass='])
    except getopt.GetoptError, e:
        usage(e)

    adminpass = ""
    sitename = ""
    dbpass = ""
    email = ""
    rootpass = ""
    rounduppass = ""
    simpleinvoicespass = ""
    tld = ""
    username = ""
    toolspass = ""

    for opt, val in opts:
        if opt in ('-a', '--apass'):
            adminpass = val
        elif  opt in ('-b', '--basesitename'):
            sitename = val
        elif opt in ('-d', '--dbpass'):
            dbpass = val
        elif opt in ('-e', '--email'):
            email = val
        elif opt in ('-p', '--pass'):
            rootpass = val
        elif opt in ('-r', '--rpass'):
            rounduppass = val
        elif opt in ('-s', '--sipass'):
            simpleinvoicespass = val
        elif opt in ('-t', '--tld'):
            tld = val
        elif opt in ('-u', '--user'):
            username = val
        elif opt in ('-z', '--zpass'):
            toolspass = val

    if not tld:
        sitename = ""
        d = Dialog('TurnKey Linux - First boot configuration')
        tld = d.get_input("Set tld (top level domain) in http://www.basesitename.TLD", "Please enter top level domain (tld) without a dot (e.g. com, org, net).")

    if not sitename:
        d = Dialog('TurnKey Linux - First boot configuration')
        sitename = d.get_input("Set base site name in http://www.BASESITENAME.%s" % tld, "Please enter base site name without 'http://www.' or '.%s'." % tld)
    
    lowername = sitename.replace(" ","").lower()
    tld = tld.lower()
    hostname = ".".join([lowername,tld])

    if not email:
        email = "@".join(['admin',hostname])

    # Set root password.
    if not username:
        username = "root"
    system("/usr/lib/inithooks/bin/setpass.py %s --pass=%s" % (username,rootpass))

    if not adminpass:
        d = Dialog('TurnKey Linux - First boot configuration')
        adminpass = d.get_password("Drupal/Solr admin and Drupal cssadmin Password", "Please enter password for the Drupal/Solr admin accounts.")

    if not dbpass:
        d = Dialog('TurnKey Linux - First boot configuration')
        dbpass = d.get_password("MySQL root Password", "Please enter password for the MySQL root account.")

    # MySQL password.
    system("/usr/lib/inithooks/bin/mysqlconf.py --user=root --pass=%s" % dbpass)

    # Roundup password.
    system("/usr/lib/inithooks/bin/roundup.py --pass=%s --email=%s" % (rounduppass,email))

    # Simple Invoices password.
    system("/usr/lib/inithooks/bin/simpleinvoices.py --pass=%s --email=%s" % (simpleinvoicespass,email))

    # Tools password.
    system("/usr/lib/inithooks/bin/tools.py --pass=%s" % toolspass)
    
    # Solr - finish password protection.
    system("touch /usr/local/solr/server/etc/realm.properties")
    system("sed -i '/admin:/d' /usr/local/solr/server/etc/realm.properties")
    system("sed -i '/drupal7:/d' /usr/local/solr/server/etc/realm.properties")
    system("echo 'admin: %s, search-role' >> /usr/local/solr/server/etc/realm.properties" % adminpass)
    system("echo 'drupal7: %s, search-role' >> /usr/local/solr/server/etc/realm.properties" % adminpass)
    system("chown -R solr:solr /usr/local/solr/server/etc")

    # Solr - finish SSL setup.
#    system("sed -i 's/>secret</>%s</g' /usr/local/solr/server/etc/jetty-https-ssl.xml" % adminpass)
#    system("keytool -genkeypair -alias solr-ssl -keyalg RSA -keysize 2048 -keypass %s -storepass %s -validity 9999 -keystore solr-ssl.keystore.jks -ext SAN=DNS:localhost,IP:127.0.0.1 -dname \"CN=localhost, OU=Manager, O=Organization, L=Location, ST=State, C=Country\"" % (adminpass,adminpass))
#    system("keytool -importkeystore -srcstorepass %s -srckeystore solr-ssl.keystore.jks -deststorepass %s -destkeystore solr-ssl.keystore.p12 -srcstoretype jks -deststoretype pkcs12" % (adminpass,adminpass))
#    system("openssl pkcs12 -in solr-ssl.keystore.p12 -passin pass:%s -out solr-ssl.pem -passout pass:%s" % (adminpass,adminpass))
#    system("mv -f solr-ssl.keystore.jks /usr/local/solr/server/etc")
#    system("mv -f solr-ssl.keystore.p12 /usr/local/solr/server/etc")
#    system("mv -f solr-ssl.pem /usr/local/solr/server/etc")

    # Solr - enable SSL.
#    system("echo 'SOLR_SSL_KEY_STORE=etc/solr-ssl.keystore.jks' >> /var/lib/solr/solr.in.sh")
#    system("echo 'SOLR_SSL_KEY_STORE_PASSWORD=%s' >> /var/lib/solr/solr.in.sh" % adminpass)
#    system("echo 'SOLR_SSL_TRUST_STORE=etc/solr-ssl.keystore.jks' >> /var/lib/solr/solr.in.sh")
#    system("echo 'SOLR_SSL_TRUST_STORE_PASSWORD=%s' >> /var/lib/solr/solr.in.sh" % adminpass)
#    system("echo 'SOLR_SSL_NEED_CLIENT_AUTH=false' >> /var/lib/solr/solr.in.sh")
#    system("echo 'SOLR_SSL_WANT_CLIENT_AUTH=false' >> /var/lib/solr/solr.in.sh")
#    system("echo 'SOLR_SSL_OPTS=\"-Djavax.net.ssl.keyStore=etc/solr-ssl.keystore.jks -Djavax.net.ssl.trustStore=etc/solr-ssl.keystore.jks\"' >> /var/lib/solr/solr.in.sh")

    # Drupal - check change admin/password.
    try:
        pwd.getpwnam('admin')
        system("echo admin:%s | chpasswd" % adminpass)
        m = MySQL()
        m.execute('SET PASSWORD FOR drupal7@localhost = PASSWORD(%s) ;' % adminpass)
    except KeyError:
        system("useradd -g root -m -s /bin/bash admin")
        system("echo admin:%s | chpasswd" % adminpass)
        m = MySQL()
        m.execute('CREATE USER drupal7@localhost IDENTIFIED BY \"%s\";' % adminpass)

    # Drupal - check change cssadmin/password with toggle to create base site.
    try:
        # Check cssadmin exists with exception if not.
        pwd.getpwnam('cssadmin')

        # Change cssadmin password.
        system("echo cssadmin:%s | chpasswd" % adminpass)

        # Base site should already exist if cssadmin exists.
        system("chmod -x /usr/lib/inithooks/firstboot.d/97formavid-base-site")

    except KeyError:
        # Create cssadmin.
        system("groupadd cssadmin")
        system("useradd -g cssadmin -m -s /bin/bash cssadmin")
        system("echo cssadmin:%s | chpasswd" % adminpass)
        system("echo 'cd /var/www/drupal7/sites/all/themes' >> /home/cssadmin/.bashrc")

        # Need to create base site.
        system("chmod +x /usr/lib/inithooks/firstboot.d/97formavid-base-site")

        # Set vars to create base site.
        system("touch /etc/inithooks.conf")
        system("echo 'DRUPAL_PASS=\"%s\"' >> /etc/inithooks.conf" % adminpass)
        system("echo 'MYSQL_PASS=\"%s\"' >> /etc/inithooks.conf" % dbpass)
        system("echo 'SITE_EMAIL=\"%s\"' >> /etc/inithooks.conf" % email)
        system("echo 'SITE_HOSTNAME=\"%s\"' >> /etc/inithooks.conf" % hostname)
        system("echo 'SITE_BASENAME=\"%s\"' >> /etc/inithooks.conf" % sitename)
        system("echo 'SITE_TLD=\"%s\"' >> /etc/inithooks.conf" % tld)

    # Switch webmin root to admin.
    # system("sed -i 's/root:/admin:/g' /etc/webmin/webmin.acl")
    # system("sed -i 's/root:/admin:/g' /etc/webmin/miniserv.users")

    # Disable root login - use admin above.
    # system("passwd -dl root")

if __name__ == "__main__":
    main()
    
