#!/usr/bin/python
# Copyright (C) 2023 Sean Borman <bormanst@gmail.com>.
# You should have received LICENSE.txt, a copy of the
# GNU General Public License, along with this program.
# If not, see <https://www.gnu.org/licenses/>.

"""

Create drupal stack

Requirements: run as root

Option:
    --apass=        unless provided, will ask interactively
    --dbpass=       unless provided, will ask interactively
    --domain=       unless provided, will ask interactively
    --email=        unless provided, will ask interactively
    --sitetitle=    unless provided, will ask interactively

"""

import datetime
import getopt
import logging
import MySQLdb as mdb
import os
import string
import sys
import yaml

from dialog_wrapper import Dialog
from local_methods import *
from subprocess import Popen, PIPE

DEFAULT_DIALOG_HEADER = "Formavid - Drupal site build script"
DEFAULT_DOMAIN = "www.examplesitename.com"
DEFAULT_LOG = "/var/log/formavid/create-drupal-stack.log"
DEFAULT_TITLE = "Example Site Name"

HTACCESS = """
# Turn off all options we don't need.
Options None
Options +FollowSymLinks

# Set the catch-all handler to prevent scripts from being executed.
SetHandler Drupal_Security_Do_Not_Remove_See_SA_2006_006
<Files *>
  # Override the handler again if we're run later in the evaluation list.
  SetHandler Drupal_Security_Do_Not_Remove_See_SA_2013_003
</Files>

# If we know how to do it safely, disable the PHP engine entirely.
<IfModule mod_php7.c>
  php_flag engine off
</IfModule>

Deny from all
"""
def main():
    try:
        opts, args = getopt.gnu_getopt(sys.argv[1:], "h", ['help', 'apass=', 'dbpass=', 'domain=', 'email=', 'formavid=', 'sitetitle='])
    except getopt.GetoptError as e:
        usage(e)

    # Log setup.
    logging.basicConfig(filename=DEFAULT_LOG,level=logging.INFO)

    # TODO: Add option to specify subdir
    drupalsubdir = "prod"

    # Sites - drupal loaction.
    drupaldir = "/".join(["/var/www/drupal9",drupalsubdir])

    # Verify default/settings.php exists.
    pathFile = "/".join([drupaldir,"web/sites/default/default.settings.php"])
    if not os.path.exists(pathFile):
        # Log start.
        logging.info('Missing requirement: %s - Missing sites/default/default.settings.php file.' % datetime.datetime.now())
        logging.info('Please verify the Drupal 9 installation in /var/www.')
        quit()

    # Log start.
    logging.info('Start time: %s' % datetime.datetime.now())

    # Get envars.
    dbpass = os.environ.get("DB_PASS")
    domain = os.environ.get("DOMAIN")
    email = os.environ.get("APP_EMAIL")
    formavid = os.environ.get("FORMAVID")
    password = os.environ.get("APP_PASS")
    sitetitle = os.environ.get("SITETITLE")

    # Check for dbpass.
    isdbpass = "DbpasswordEnvar"
    if not dbpass or dbpass == "None": isdbpass = "No-DbpasswordEnvar"

    # Check for password.
    ispassword = "PasswordEnvar"
    if not password or password == "None": ispassword = "No-PasswordEnvar"

    # Log envars.
    logging.info('Incoming envars: [isdbpass]:[domain]:[email]:[formavid]:[ispassword]:[sitetitle]')
    logging.info('Incoming envars: [%s]:[%s]:[%s]:[%s]:[%s]:[%s]' % (isdbpass, domain, email, formavid, ispassword, sitetitle))

    # Assign common dialog header.
    d = Dialog(DEFAULT_DIALOG_HEADER)

    # List of modules to enable: initially populated by bin/deploy/shell/default_envars script.
    modulesToEnable = []
    logging.info('Drupal modules to enable: %s' % modulesToEnable)

    # Check inputs.
    for opt, val in opts:
        if opt in ('-h', '--help'):
            usage()
        elif opt == '--apass':
            password = val
        elif opt == '--dbpass':
            dbpass = val
        elif opt == '--domain':
            domain = val
        elif opt == '--email':
            email = val
        elif opt == '--formavid':
            formavid = val
        elif opt == '--sitetitle':
            sitetitle = val

    # Get formavid location.
    if not formavid or formavid == "None": formavid = "/usr/local/formavid"

    # Get domain.
    if not domain or domain == "None":
        domain = d.get_input(
            "Add drupal9 Domain",
            "Enter additional domain for drupal9.",
            DEFAULT_DOMAIN)

    # Format domain.
    domain = format_domain(domain)

    # Get hostname.
    hostname = get_hostname(domain)

    # Get sitename.
    sitename = get_sitename(domain)

    # Check hostname already exists.
    pathFile = "/".join([drupaldir,"web/sites",hostname])
    if os.path.exists(pathFile):
        # Log error.
        logging.info('Selected domain already has Drupal 9 site: %s - Check sites/%s directory.' % (datetime.datetime.now(),hostname))
        logging.info('Site stack creation for %s has been cancelled.' % hostname)
        quit()

    # Get site title.
    if not sitetitle or sitetitle == "None":
        sitetitle = d.get_input(
            "Enter Drupal 9 Site Title",
            "Enter title for new drupal9 site.",
            DEFAULT_TITLE)

    # Get admin email.
    if not email or email == "None":
        email = d.get_email(
            "Enter Drupal 9 admin Email",
            "Please enter email address for the Drupal 9 admin account.",
            "admin@%s" % get_hostname(domain))

    if not dbpass or dbpass == "None":
        dbpass = d.get_password(
            "Warning - verify resources exist for additional site.",
            "Please enter password for the MySQL root account.")

    if not password or password == "None":
        password = d.get_password(
            "Warning - verify resources exist for additional site.",
            "Please enter password for the drupal9 admin account.")

    # Log vars.
    logging.info('Vars used to create stack: [isdbpass]:[domain]:[email]:[formavid]:[hostname]:[ispassword]:[sitename]:[sitetitle]')
    logging.info('Vars used to create stack: [%s]:[%s]:[%s]:[%s]:[%s]:[%s]:[%s]:[%s]' % (isdbpass, domain, email, formavid, hostname, ispassword, sitename, sitetitle))

    # Log create start.
    logging.info('Starting stack creation: %s' % datetime.datetime.now())

    # Start default site setup.
    system("echo ''")
    system("echo ''")
    system("echo ''")
    system("echo 'Creating default site for %s - this takes a while ...'" % hostname)
    system("echo ''")

    # Sites - templates location.
    templates = formavid

    # Sites - ensure clean start.
    system("rm -rf %s/sites-staging" % templates)

    # Sites - set types.
    # siteTypes = ['article','aggregator','blog','book','forum','poll']
    siteTypes = ['article']

    # Hosts - update.
    for sitetype in siteTypes:
        sitetypemod = ''
        if sitetype != 'article':
            sitetypemod = sitetype + '.'
        system("sed -i '/127.0.0.1/s/$/ %s%s/' /etc/hosts" % (sitetypemod,hostname))
        # Log info.
        logging.info('/etc/hosts configuration is complete.')

    # Sites - prepare templates.
    system("cp -rf /etc/formavid/templates/sites-template %s/sites-staging" % templates)

    # Apache - replace sitehostname in confs.
    system("find %s/sites-staging -name \"*.conf\" -exec sed -i \"s/sitehostname/%s/g\" '{}' \\;" % (templates,hostname))

    # Apache - replace drupalsubdir in confs.
    system("find %s/sites-staging -name \"*.conf\" -exec sed -i \"s/drupalsubdir/%s/g\" '{}' \\;" % (templates,drupalsubdir))

    # Apache - add sites available.
    system("cp -f %s/sites-staging/sitehostname.conf /etc/apache2/sites-available/%s.conf" % (templates,hostname))

    # Apache - enable added sites.
    system("cp -sf /etc/apache2/sites-available/%s.conf /etc/apache2/sites-enabled/." % hostname)

    # Sites - replace sitethemename in js.
    system("find %s/sites-staging -name \"*.js\" -exec sed -i \"s/sitethemename/%s/g\" '{}' \\;" % (templates,sitename))

    # Set root owner for sites/themes.
    system("chown root:root %s/web/themes" % drupaldir)

    # Set first site flag.
    firstSite = False
    pathFile = "/".join([drupaldir,"web/sites/sites.php"])
    if not os.path.exists(pathFile): firstSite = True

    # Create drupal sites.
    os.chdir(drupaldir)
    for sitetype in siteTypes:
        sitetypemod = ''
        sitetypetitle = ''
        if sitetype != 'article':
            sitetypemod = sitetype + '.'
            sitetypetitle = ' ' + sitetype.title() + 's'
        baseUri = sitetypemod + hostname
        # Create site type.
        system("echo ''")
        system("echo 'Creating %s drupal site ...'" % baseUri)
        system("echo ''")
        system("drush --root=\"%s\" --uri=\"http://%s\" si standard --yes --db-url=\"mysql://admin:%s@localhost:3306/%s_%s\" --account-name=\"admin\" --account-mail=\"admin@%s\" --site-mail=\"admin@%s\" --account-pass=\"%s\" --locale=\"en\" --site-name=\"%s\" --site-pass=\"%s\" --sites-subdir=\"%s\"" % (drupaldir,baseUri,password,sitename,sitetype,baseUri,baseUri,password,sitetitle,password,baseUri))
        system("mkdir -p %s/web/sites/%s/files/background_image/css" % (drupaldir,baseUri))
        system("chmod 0775 -R %s/web/sites/%s/files/background_image" % (drupaldir,baseUri))
        system("chown admin:admin -R %s/web/sites/%s/files/background_image" % (drupaldir,baseUri))
        system("chmod 0777 %s/web/sites/%s/files" % (drupaldir,baseUri))
        # Sites - set trusted_host_patterns.
        esc_baseUri = baseUri.replace(".","\\\\\.")
        new_lines="\$settings['trusted_host_patterns'] = array\(\\n\\t'^" + esc_baseUri + "\$',\\n\);\\n"
        system("sed -i \"/trusted_host_patterns/,/\*\//{n;s|^$|%s|}\" %s/web/sites/%s/settings.php" % (new_lines,drupaldir,hostname))
        # Sites - set private file path.
        system("sed -i \"s/\#\ \$settings\['file_private_path']\ =\ '';/\$settings\['file_private_path']\ =\ 'sites\/%s\/files\/private';/g\" %s/web/sites/%s/settings.php" % (hostname,drupaldir,hostname))
        # Sites - set database init commands.
        system("sed -i \"/'autoload' => 'core\/modules\/mysql\/src\/Driver\/Database\/mysql\/',/a\  'init_commands' => ['isolation_level' => 'SET SESSION TRANSACTION ISOLATION LEVEL READ COMMITTED',],\" %s/web/sites/%s/settings.php" % (drupaldir,hostname))
        # Sites - update settings.
        system("chmod 0444 %s/web/sites/%s/settings.php" % (drupaldir,baseUri))
        system("echo ''")
        system("echo 'The drupal site %s has been created.'" % baseUri)
        system("echo ''")
        # Log info.
        logging.info('The drupal site %s has been created.' % baseUri)

    try:
        # Get db conection.
        con = mdb.connect(host="localhost", user="root", passwd="%s" % dbpass)
        # Get db cursor.
        cur = con.cursor()
        # Sites - set additional database properties.
        for sitetype in siteTypes:
            # Allow perms for drush.
            cur.execute("GRANT ALL PRIVILEGES ON %s_%s.* TO drupal9@localhost WITH GRANT OPTION; FLUSH PRIVILEGES;" % (sitename,sitetype))
            # Log info.
            logging.info('Allow perms for drush db access on %s_%s.*.' % (sitename,sitetype))
        # Restart mysql.
        system("echo ''")
        system("echo 'Restarting mysql service ...'")
        system("echo ''")
        system("systemctl restart mysql")
        system("echo ''")

    except mdb.Error as e:
#        print "Error %d: %s" % (e.args[0],e.args[1])
        sys.exit(1)

    finally:
        if con:
            con.close()

    # Restart apache2.
    system("echo ''")
    system("echo 'Restarting apache2 service ...'")
    system("echo ''")
    system("systemctl restart apache2")
    system("echo ''")

    # Clear drupal caches.
    for sitetype in siteTypes:
        sitetypemod = ''
        if sitetype != 'article':
            sitetypemod = sitetype + '.'
        baseUri = sitetypemod + hostname
        system("echo ''")
        system("echo 'Rebuilding %s drupal caches ...'" % baseUri)
        system("drush --root=\"%s\" --uri=\"http://%s\" cache:rebuild --yes" % (drupaldir,baseUri))
        system("echo 'Site %s can now be modified.'" % baseUri)

    # Start configuring drupal.
    system("echo ''")
    system("echo ''")
    system("echo 'Creating custom theme for %s based on zen theme ...'" % sitetitle)
    system("echo ''")

    # Site theme location.
    siteTheme = "%s/web/themes/%s" % (drupaldir,sitename)

    # Enable zen theme.
    system("drush --root=\"%s\" --uri=\"http://%s\" theme:enable -y zen" % (drupaldir,hostname))

    # Create site sub-theme from zen theme.
    system("cp -fpr %s/web/themes/contrib/zen/STARTERKIT %s/web/themes" % (drupaldir,drupaldir))
    system("mv %s/web/themes/STARTERKIT %s" % (drupaldir,siteTheme))
    system("find %s -name \"*STARTERKIT*\" -exec bash -c 'mv $0 ${0/STARTERKIT/%s}' {} \;" % (siteTheme,sitename))
    system("find %s -type f -exec sed -i 's/STARTERKIT/%s/g' {} \;" % (siteTheme,sitename))
    system("find %s -type f -exec sed -i 's/Zen\ Sub-theme\ Starter\ Kit/%s/g' {} \;" % (siteTheme,sitetitle))
    
    system("find %s -type f -exec sed -i 's/Zen\ Sub-theme\ Starter\ Kit/%s/g' {} \;" % (siteTheme,sitetitle))
    
    system("echo ''")
    system("echo 'Theme %s is ready for modification.'" % sitename)
    system("echo ''")

    # Set system theme if first site.
    if firstSite:
        # Symlink system theme to first theme.
        system("echo ''")
        system("echo 'Symlinking system theme to %s theme ...'" % sitename)
        system("echo ''")
        sysTheme = "%s/web/themes/system" % (drupaldir)
        system("rm -f %s" % sysTheme)
        system("ln -s %s %s" % (siteTheme,sysTheme))
        # Symlink system theme to admin pages.
        appDir = "/var/www/admin"
        if os.path.exists(appDir):
            appTheme = "/".join([appDir,"theme"])
            system("ln -s %s %s" % (sysTheme,appTheme))
        # Symlink system theme to support pages.
        appDir = "/var/www/support/html"
        if os.path.exists(appDir):
            appTheme = "/".join([appDir,"theme"])
            system("ln -s %s %s" % (sysTheme,appTheme))
        # Symlink system theme to webmin - used in apllications/webmin/webmin as well
        appDir = "/usr/share/webmin/system-theme/unauthenticated"
        if os.path.exists(appDir):
            appTheme = "/".join([appDir,"system"])
            system("ln -s %s %s" % (sysTheme,appTheme))

    # Check local gulp for SASS.
    gulpFile = "%s/gulpfile.js" % siteTheme
    if os.path.exists(gulpFile):
        # Set local gulp for SASS.
        system("echo ''")
        system("echo 'Setting up local Gulp for %s theme ...'" % sitename)
        system("cp -f %s/sites-staging/gulpfile.js %s" % (templates,siteTheme))
        system("echo 'Gulp ready to run locally within theme directory.'")
        # Set prettier compatibility.
        system("echo ''")
        system("echo 'Setting up prettier compatibility for %s theme ...'" % sitename)
        system("sed -i 's/\"anonymous\": \"always\",/\"anonymous\": \"never\",/g' %s/.eslintrc" % siteTheme)
        system("sed -i 's/no-empty-rulesets: 2/no-empty-rulesets: 1/g' %s/.sass-lint.yml" % siteTheme)
        system("echo 'bracketSpacing: false' >> %s/.prettierrc" % siteTheme)
        system("echo 'endOfLine: lf' >> %s/.prettierrc" % siteTheme)
        system("echo 'singleQuote: true' >> %s/.prettierrc" % siteTheme)
        system("echo 'Gulp prettier compatibility completed.'")
        # Pretty up zen theme.
        system("echo ''")
        system("echo 'Prettying up %s theme files ...'" % sitename)
        scssFile = "%s/components/init/clearfix/_clearfix.scss" % siteTheme
        if os.path.exists(scssFile):
            system("sed -i 's/\&:after/\&::after/g' %s" % scssFile)
            system("sed -i 's/\&:before/\&::before/g' %s" % scssFile)
        scssFile = "%s/components/base/forms/_forms.scss" % siteTheme
        if os.path.exists(scssFile):
            system("sed -i 's/\*/\/\/ \*/g' %s" % scssFile)
        scssFile = "%s/components/base/links/_links.scss" % siteTheme
        if os.path.exists(scssFile):
            system("sed -i 's/href\]:after/href\]::after/g' %s" % scssFile)
            system("sed -i \"s/'javascript:'\]:after/'javascript:'\]::after/g\" %s" % scssFile)
            system("sed -i \"s/'#'\]:after/'#'\]::after/g\" %s" % scssFile)
        scssFile = "%s/components/base/text/_text.scss" % siteTheme
        if os.path.exists(scssFile):
            system("sed -i 's/\&:after/\&::after/g' %s" % scssFile)
#        system("gulp -f %s fix-js" % gulpFile)
        system("echo 'Prettying up theme files completed.'")

    # Drupal - init git site theme.
    gitDir = "/".join(["/var/lib/git/drupal9",drupalsubdir,"web/themes",sitename])
    system("mkdir -p %s" % gitDir)
    system("echo 'components/asset-builds' >> %s/.gitignore" % siteTheme)
    system("echo 'styleguide' >> %s/.gitignore" % siteTheme)
    system("git -C %s init --separate-git-dir=%s" % (siteTheme,gitDir))
    system('git -C %s config user.email "cssadmin@modorbis.com"' % siteTheme)
    system('git -C %s config user.name "cssadmin"' % siteTheme)

    # Drupal - set site theme permissions.
    system("chown -R cssadmin:cssadmin %s" % siteTheme)
    system("find %s -type d -name \* -exec chmod 0755 {} \;" % siteTheme)
    pathDir = "%s/components/asset-builds" % siteTheme
    if os.path.exists(pathDir):
        system("find %s -type d -name \* -exec chmod 0777 {} \;" % pathDir)
    pathDir = "%s/styleguide" % siteTheme
    if os.path.exists(pathDir):
        system("chmod 0777 %s" % pathDir)

    # Drupal - git commit site theme.
    system('git -C %s add .' % siteTheme)
    system('git -C %s commit -m "Initial commit by site creation script."' % siteTheme)
    system("chown -R cssadmin:cssadmin %s" % gitDir)

    # Drupal - enable/disable properties.
    for sitetype in siteTypes:
        sitetypemod = ''
        if sitetype != 'article':
            sitetypemod = sitetype + '.'
        baseUri = sitetypemod + hostname
        # Start configuring sites.
        system("echo ''")
        system("echo ''")
        system("echo 'Enabling and disabling Drupal properties for %s ...'" % sitetitle)
        system("echo ''")
        # Enable modules.
        system("drush --root=\"%s\" --uri=\"http://%s\" pm:enable %s --yes" % (drupaldir,baseUri," ".join(modulesToEnable)))
        # Install sub-theme prior to possible disabling default search - fails otherwise.
        system("drush --root=\"%s\" --uri=\"http://%s\" theme:enable %s --yes" % (drupaldir,baseUri,sitename))
        system("drush --root=\"%s\" --uri=\"http://%s\" config:set system.theme default %s --yes" % (drupaldir,baseUri,sitename))

        # Set configs.
        system("drush --root=\"%s\" --uri=\"http://%s\" config:set --yes block.block.%s_powered status 0" % (drupaldir,baseUri,sitename))
        # Clean up.
        system("echo ''")
        system("echo 'Rebuilding %s drupal caches ...'" % baseUri)
        system("drush --root=\"%s\" --uri=\"http://%s\" cache:rebuild --yes" % (drupaldir,baseUri))
        system("echo ''")
        system("echo 'Rebuilding %s drupal content permissions ...'" % baseUri)
        system("drush --root=\"%s\" --uri=\"http://%s\" php-eval \"node_access_rebuild();\"" % (drupaldir,baseUri))
        system("echo ''")
        system("echo 'Finishing setup of drupal files directory for %s ...'" % baseUri)
        # Make private dir and set .htaccess file.
        system("mkdir -p %s/web/sites/%s/files/private" % (drupaldir,baseUri))
        system("echo \"%s\" >  %s/web/sites/%s/files/private/.htaccess" % (HTACCESS,drupaldir,baseUri))
        system("chmod 0444 %s/web/sites/%s/files/private/.htaccess" % (drupaldir,baseUri))
        # Set admin owner all.
        system("chown -R admin:admin %s/web/sites/%s" % (drupaldir,baseUri))
        # Set individual perms.
        system("mkdir -p %s/web/sites/%s/files/css" % (drupaldir,baseUri))
        system("chmod 0775 %s/web/sites/%s/files/css" % (drupaldir,baseUri))
        system("chown -R www-data:www-data %s/web/sites/%s/files/css" % (drupaldir,baseUri))
        system("mkdir -p %s/web/sites/%s/files/js" % (drupaldir,baseUri))
        system("chmod 0775 %s/web/sites/%s/files/js" % (drupaldir,baseUri))
        system("chown -R www-data:www-data %s/web/sites/%s/files/js" % (drupaldir,baseUri))
        system("mkdir -p %s/web/sites/%s/files/php" % (drupaldir,baseUri))
        system("chmod 0777 %s/web/sites/%s/files/php" % (drupaldir,baseUri))
        system("chown -R www-data:www-data %s/web/sites/%s/files/php" % (drupaldir,baseUri))
        system("chown www-data:www-data %s/web/sites/%s/files/private" % (drupaldir,baseUri))
        system("chmod 0750 %s/web/sites/%s/files/private" % (drupaldir,baseUri))
        system("mkdir -p %s/web/sites/%s/files/styles" % (drupaldir,baseUri))
        system("chmod 0775 %s/web/sites/%s/files/styles" % (drupaldir,baseUri))
        system("chown -R www-data:www-data %s/web/sites/%s/files/styles" % (drupaldir,baseUri))
        system("echo 'Completed setup of drupal site %s files directory.'" % baseUri)
        system("echo ''")
        system("echo 'Running initial cron job for drupal site %s ...'" % baseUri)
        system("echo ''")
        # Finished drupal setup.
        system("echo 'Please validate %s by viewing the drupal admin status report.'" % baseUri)
        if not os.path.exists("/var/www/admin/images/%s.svg" % sitename):
            system("ln -s %s/logo.svg /var/www/admin/images/%s.svg" % (siteTheme,sitename))
        # Log info.
        logging.info('Drupal site created/configured for %s.' % baseUri)

    # Sites - clean up.
    system("rm -rf %s/sites-staging" % templates)

    # Set admin owner for sites/themes.
    system("chown admin:admin %s/web/sites" % drupaldir)
    system("chown admin:admin %s/web/sites/sites.php" % drupaldir)
    system("chown cssadmin:cssadmin %s/web/themes" % drupaldir)

    # Check formavid logo.
    if not sitename == "formavidorg":
        # Set theme.
        lnLoc = "ln -sf %s" % siteTheme
        # Admin Tools - use first "base" site logo.
        lnFile = "logo.svg"
        pathDir = "/var/www/admin/images"
        pathFile = ''.join([pathDir,'/',lnFile])
        if os.path.exists(pathDir) and not os.path.exists(pathFile):
            # Symlink logo to admin pages.
            system("%s/%s %s" % (lnLoc,lnFile,pathFile))

    # Postfix - add virtual addresses.
    system("echo ''")
    system("echo ''")
    system("echo 'Adding %s email addresses to postfix ...'" % hostname)
    system("echo ''")
    system("echo 'admin@%s admin' >> /etc/postfix/virtual" % hostname)
    system("echo 'support@%s admin' >> /etc/postfix/virtual" % hostname)
    system("postmap /etc/postfix/virtual")
    system("echo ''")
    system("echo 'Postfix has been updated.'")
    # Log info.
    logging.info('Postfix has been updated.')

    # End default site setup.
    system("echo ''")
    system("echo ''")
    system("echo 'Default site setup for %s is complete.'" % sitetitle)
    system("echo ''")
    system("echo ''")

    # Log end.
    logging.info('Completed stack creation for %s: %s' % (hostname, datetime.datetime.now()))

if __name__ == "__main__":
    main()
