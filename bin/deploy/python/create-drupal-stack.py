#!/usr/bin/python
# Copyright (C) 2018 Sean Borman <bormanst@gmail.com>.
# You should have received LICENSE.txt, a copy of the
# GNU General Public License, along with this program.
# If not, see <https://www.gnu.org/licenses/>.

"""

Create drupal stack

Option:
    --apass=        unless provided, will ask interactively
    --dbpass=       unless provided, will ask interactively
    --domain=       unless provided, will ask interactively
    --email=        unless provided, will ask interactively
    --sitetitle=    unless provided, will ask interactively
    --solr=         unless provided, will ask interactively

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

# Sets the site specific default solr configurations.
def set_solr_configs(solrconfigpath, solrserverid, solrservername, solrcorename, password, formavid):

    # Get solr server config file.
    with open(solrconfigpath + '/search_api.server.default_solr_server.yml') as f:
        doc = yaml.safe_load(f)

    # Set configs.
    doc['id'] = solrserverid + "_solr_server"
    doc['name'] = solrservername + " Solr Server"
    doc['description'] = "Configured by site creation script located in %s/bin" % formavid
    doc['backend_config']['connector'] = "basic_auth"
    doc['backend_config']['connector_config']['core'] = solrcorename
    doc['backend_config']['connector_config']['password'] = password
    doc['backend_config']['connector_config']['username'] = "drupal8"

    # Write updated solr server config file.
    with open(solrconfigpath + '/search_api.server.default_solr_server.yml', 'w') as f:
        yaml.safe_dump(doc, f, default_flow_style=False)

    # Get solr index config file.
    with open(solrconfigpath + '/search_api.index.default_solr_index.yml') as f:
        doc = yaml.safe_load(f)

    # Set configs.
    doc['id'] = solrserverid + "_solr_index"
    doc['name'] = solrservername + " Solr content index"
    doc['description'] = "Configured by site creation script located in %s/bin" % formavid
    doc['server'] = solrserverid + "_solr_server"

    # Write updated solr index config file.
    with open(solrconfigpath + '/search_api.index.default_solr_index.yml', 'w') as f:
        yaml.safe_dump(doc, f, default_flow_style=False)

DEFAULT_DIALOG_HEADER = "Formavid - Drupal site build script"
DEFAULT_DOMAIN = "www.examplesitename.com"
DEFAULT_LOG = "/var/log/formavid/create-drupal-stack.log"
DEFAULT_TITLE = "Example Site Name"

SOLR_TEXT = """Solr search can be used as a replacement for core content search and boasts both extra features and better performance. Low memory systems may wish to use the default search to avoid the overhead associated with a Java virtual machine."""

GULP_WATCH_SCSS_SCRIPT = """
// #########################################################
// ONLY watches for changed scss files.
// JS files and the style guide require the regular gulp
// watch to compile any updates. It is recommended to run
// the regular watch after theming is completed.
// #########################################################
gulp.task('watch-scss', ['watch:css', 'lint:sass']);
"""

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
        opts, args = getopt.gnu_getopt(sys.argv[1:], "h", ['help', 'apass=', 'dbpass=', 'domain=', 'email=', 'formavid=', 'sitetitle=', 'solr='])
    except getopt.GetoptError, e:
        usage(e)

    # Log setup.
    logging.basicConfig(filename=DEFAULT_LOG,level=logging.INFO)

    # TODO: Add option to specify subdir
    drupalsubdir = "prod"

    # Sites - drupal loaction.
    drupaldir = "/".join(["/var/www/drupal8",drupalsubdir])

    # Verify default/settings.php exists.
    pathFile = "/".join([drupaldir,"web/sites/default/default.settings.php"])
    if not os.path.exists(pathFile):
        # Log start.
        logging.info('Missing requirement: %s - Missing sites/default/default.settings.php file.' % datetime.datetime.now())
        logging.info('Please verify the drupal 8 installation in /var/www.')
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
    solr = os.environ.get("SOLR_INSTALL")
    solrnew = os.environ.get("SOLR_NEW")

    # Check for dbpass.
    isdbpass = "DbpasswordEnvar"
    if not dbpass or dbpass == "None": isdbpass = "No-DbpasswordEnvar"

    # Check for password.
    ispassword = "PasswordEnvar"
    if not password or password == "None": ispassword = "No-PasswordEnvar"

    # Log envars.
    logging.info('Incoming envars: [isdbpass]:[domain]:[email]:[formavid]:[ispassword]:[sitetitle]:[solr]')
    logging.info('Incoming envars: [%s]:[%s]:[%s]:[%s]:[%s]:[%s]:[%s]' % (isdbpass, domain, email, formavid, ispassword, sitetitle, solr))

    # Assign common dialog header.
    d = Dialog(DEFAULT_DIALOG_HEADER)

    # List of solr related modules.
    solrModules = ['search_api_solr', 'search_api_solr_defaults']
    logging.info('Drupal solr related modules: %s' % solrModules)

    # List of modules to enable: initially populated by applications/1000-drupal8/drupal8drupal8 script.
    modulesToEnable = ['advagg','advanced_help','background_image','backup_migrate','captcha','components','ctools','devel','features','field_group','fivestar','honeypot','image_style_quality','imageapi_optimize','imagemagick','imce','inline_entity_form','module_filter','panels','pathauto','recaptcha','rules','search_api_solr','search_api_solr_defaults','tagadelic','views_bulk_operations']
    logging.info('Drupal modules to enable: %s' % modulesToEnable)

    # Remove solr related modules from enable list.
    for module in solrModules:
        if module in modulesToEnable:
            modulesToEnable.remove(module)

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
        elif opt == '--solr':
            solr = val
        elif opt == '--solrpass':
            solrnew = val

    # Get formavid location.
    if not formavid or formavid == "None": formavid = "/usr/local/formavid"

    # Get domain.
    if not domain or domain == "None":
        domain = d.get_input(
            "Add Drupal8 Domain",
            "Enter additional domain for Drupal8.",
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
        logging.info('Selected domain already has drupal8 site: %s - Check sites/%s directory.' % (datetime.datetime.now(),hostname))
        logging.info('Site stack creation for %s has been cancelled.' % hostname)
        quit()

    # Get site title.
    if not sitetitle or sitetitle == "None":
        sitetitle = d.get_input(
            "Enter Drupal8 Site Title",
            "Enter title for new Drupal8 site.",
            DEFAULT_TITLE)

    # Get admin email.
    if not email or email == "None":
        email = d.get_email(
            "Enter Drupal8 admin Email",
            "Please enter email address for the Drupal8 admin account.",
            "admin@%s" % get_hostname(domain))

    # Check solr install.
    installSolr = False
    if not solr or solr == "None":
        installSolr = not d.yesno(
            "Select drupal's search type:",
            SOLR_TEXT,
            "Default",
            "Solr")
    elif solr == "True": installSolr = True

    # Check solr requirements.
    if installSolr:
        # Check solr service available.
        system("systemctl enable solr")
        system("systemctl start solr")
        subproc = Popen(['systemctl', 'is-active', 'solr'], stdout=PIPE, stderr=PIPE)
        out, err = subproc.communicate()
        if out and out.strip().lower() != 'active':
            system("echo ''")
            system("echo ''")
            system("echo 'You selected Solr search but the solr service is not available!!!'")
            system("echo 'Please validate that your Solr service is available prior to running this script.'")
            system("echo 'Solr info is available on the admin/tools page.'")
            system("echo 'Try starting solr with `systemctl start solr` and `systemctl enable solr` to autostart on boot.'")
            system("echo ''")
            system("echo 'If desired, select the default search and manually enable solr later.'")
            system("echo ''")
            system("echo 'Exiting Drupal site build script with no action taken.'")
            system("echo ''")
            # Log info.
            logging.info('You selected Solr search but the solr service is not available!!!')
            quit()
        if not solrnew or solrnew == "None":
            solrnew = d.get_password(
                "Solr server access.",
                "Please enter Solr password for the drupal8 account.")

    if not dbpass or dbpass == "None":
        dbpass = d.get_password(
            "Warning - verify resources exist for additional site.",
            "Please enter password for the MySQL root account.")

    if not password or password == "None":
        password = d.get_password(
            "Warning - verify resources exist for additional site.",
            "Please enter password for the Drupal8 admin account.")

    # Log vars.
    logging.info('Vars used to create stack: [isdbpass]:[domain]:[email]:[formavid]:[hostname]:[ispassword]:[sitename]:[sitetitle]:[installSolr]')
    logging.info('Vars used to create stack: [%s]:[%s]:[%s]:[%s]:[%s]:[%s]:[%s]:[%s]:[%s]' % (isdbpass, domain, email, formavid, hostname, ispassword, sitename, sitetitle, installSolr))

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

    # Check if solr needs configuration.
    if installSolr:
        # Solr - set core properties.
        system("echo ''")
        system("echo 'Configuring solr search core data ...'")
        system("echo ''")
        # Solr - create template dir.
        system("mkdir -p %s/%s" % (templates,sitename))
        for sitetype in siteTypes:
            system("mkdir -p %s/%s/%s" % (templates,sitename,sitetype))
            system("cp -f /etc/formavid/templates/cores-template/core.properties.template %s/%s/%s/core.properties" % (templates,sitename,sitetype))
            system("sed -i \"s/sedsitename/%s/g\" %s/%s/%s/core.properties" % (sitename,templates,sitename,sitetype))
            system("sed -i \"s/sedsitetype/%s/g\" %s/%s/%s/core.properties" % (sitetype,templates,sitename,sitetype))
        # Solr - load cores.
        solrdata = "/var/lib/solr/data"
        system("mv %s/%s %s" % (templates,sitename,solrdata))
        # Solr - copy drupal solr conf.
        apachesolr = "/".join([drupaldir,"web/modules/contrib/search_api_solr/solr-conf/7.x"])
        for sitetype in siteTypes:
            system("cp -r %s %s/%s/%s/conf" % (apachesolr,solrdata,sitename,sitetype))
            system("sed -i \"s|solr.install.dir=.*|solr.install.dir=/usr/local/solr|g\" %s/%s/%s/conf/solrcore.properties" % (solrdata,sitename,sitetype))
        # Solr - ensure owner.
        system("chown -R solr:solr %s/%s" % (solrdata,sitename))
        # Solr - enable changes.
        system("systemctl restart solr")
        system("echo ''")
        system("echo 'Solr search core data configuration is complete.'")
        system("echo ''")
        # Log info.
        logging.info('Solr search core data configuration is complete.')

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
        system("drupal --root=%s multisite:new  %s http://%s --copy-default --uri=\"http://%s\"" % (drupaldir,baseUri,baseUri,baseUri))
        system("drupal --root=%s --uri=\"http://%s\" site:install:inline --profile=\"standard\" --langcode=\"en\" --db_type=\"mysql\" --db_host=\"127.0.0.1\" --db_name=\"%s_%s\" --db_user=\"admin\" --db_pass=\"%s\" --db_port=\"3306\" --site_name=\"%s\" --site_mail=\"admin@%s\" --account_name=\"admin\" --account_mail=\"admin@%s\" --account_pass=\"%s\"" % (drupaldir,baseUri,sitename,sitetype,password,sitetitle,hostname,hostname,password))
        system("chmod 0777 %s/web/sites/%s/files" % (drupaldir,baseUri))
        system("chmod 0444 %s/web/sites/%s/settings.php" % (drupaldir,baseUri))
        # Sites - set trusted_host_patterns.
        esc_baseUri = baseUri.replace(".","\\\\\.")
        new_lines="\$settings['trusted_host_patterns'] = array\(\\n\\t'^" + esc_baseUri + "\$',\\n\);\\n"
        system("sed -i \"/trusted_host_patterns/,/\*\//{n;s|^$|%s|}\" %s/web/sites/%s/settings.php" % (new_lines,drupaldir,hostname))
        # Sites - set private file path.
        system("sed -i \"s/\#\ \$settings\['file_private_path']\ =\ '';/\$settings\['file_private_path']\ =\ 'sites\/%s\/files\/private';/g\" %s/web/sites/%s/settings.php" % (hostname,drupaldir,hostname))
        # Sites - update settings.
        system("echo ''")
        system("echo 'The drupal site %s has been created.'" % baseUri)
        system("echo ''")
        # Log info.
        logging.info('The drupal site %s has been created.' % baseUri)

    # Sites - clean up.
    system("rm -rf %s/sites-staging" % templates)

    try:
        # Get db conection.
        con = mdb.connect(host="localhost", user="root", passwd="%s" % dbpass)
        # Get db cursor.
        cur = con.cursor()
        # Sites - set additional database properties.
        for sitetype in siteTypes:
            # Allow perms for drush.
            cur.execute("GRANT ALL PRIVILEGES ON %s_%s.* TO drupal8@localhost WITH GRANT OPTION; FLUSH PRIVILEGES;" % (sitename,sitetype))
            # Log info.
            logging.info('Allow perms for drush db access on %s_%s.*.' % (sitename,sitetype))
        # Restart mysql.
        system("echo ''")
        system("echo 'Restarting mysql service ...'")
        system("echo ''")
        system("systemctl restart mysql")
        system("echo ''")

    except mdb.Error, e:
        print "Error %d: %s" % (e.args[0],e.args[1])
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
        system("drupal --root=%s --uri=\"http://%s\" cache:rebuild" % (drupaldir,baseUri))
        system("echo 'Site %s can now be modified.'" % baseUri)

    # Start configuring drupal.
    system("echo ''")
    system("echo ''")
    system("echo 'Creating custom theme for %s based on zen theme ...'" % sitetitle)
    system("echo ''")

    # Enable zen theme.
    system("drush -r %s -l http://%s theme:enable -y zen" % (drupaldir,hostname))

    # Create site sub-theme from zen theme.
    system("cp -fpr %s/web/themes/contrib/zen/STARTERKIT %s/web/themes" % (drupaldir,drupaldir))
    system("mv %s/web/themes/STARTERKIT %s/web/themes/%s" % (drupaldir,drupaldir,sitename))
    system("find %s/web/themes/%s -iname \"*STARTERKIT*\" -exec rename 's/STARTERKIT/%s/' {} \;" % (drupaldir,sitename,sitename))
    system("find %s/web/themes/%s -type f -exec sed -i 's/STARTERKIT/%s/g' {} \;" % (drupaldir,sitename,sitename))
    system("find %s/web/themes/%s -type f -exec sed -i 's/Zen\ Sub-theme\ Starter\ Kit/%s/g' {} \;" % (drupaldir,sitename,sitetitle))
    system("echo ''")
    system("echo 'Theme %s is ready for modification.'" % sitename)
    system("echo ''")

    # Set system theme if first site.
    if firstSite:
        # Symlink system theme to first theme.
        system("echo ''")
        system("echo 'Symlinking system theme to %s theme ...'" % sitename)
        system("echo ''")
        firstTheme = "%s/web/themes/%s" % (drupaldir,sitename)
        sysTheme = "%s/web/themes/system" % (drupaldir)
        system("rm -f %s" % sysTheme)
        system("ln -s %s %s" % (firstTheme,sysTheme))

    # Set local gulp for SASS.
    system("echo ''")
    system("echo 'Setting up local Gulp for %s theme ...'" % sitename)
    system("sed -i \"s/^[[:space:]]*'use strict';/\/\/\ 'use strict'/g\" %s/web/themes/%s/gulpfile.js" % (drupaldir,sitename))
    system("sed -i \"s/options.drupalURL\ =\ ''\;/options.drupalURL\ =\ 'http:\/\/%s'\;/\" %s/web/themes/%s/gulpfile.js" % (hostname,drupaldir,sitename))
    system("sed -i \"s/node_modules\//..\/node_modules\//g\" %s/web/themes/%s/gulpfile.js" % (drupaldir,sitename))
    system("echo \"%s\" >>  %s/web/themes/%s/gulpfile.js" % (GULP_WATCH_SCSS_SCRIPT,drupaldir,sitename))
    system("echo 'Gulp ready to run locally within theme directory.'")

    # Drupal - set site theme permissions.
    system("chown -R cssadmin:cssadmin %s/web/themes/%s" % (drupaldir,sitename))
    system("find %s/web/themes/%s -type d -name \* -exec chmod 0755 {} \;" % (drupaldir,sitename))
    system("find %s/web/themes/%s/components/asset-builds -type d -name \* -exec chmod 0777 {} \;" % (drupaldir,sitename))
    system("chmod 0777 %s/web/themes/%s/styleguide" % (drupaldir,sitename))

    # Set path to solr configs.
    solrconfigpath = "/".join([drupaldir,"web/modules/contrib/search_api_solr/search_api_solr_defaults/config/optional"])

    # Drupal - enable/disable properties.
    for sitetype in siteTypes:
        sitetypemod = ''
        solrserverid = sitename
        solrcorename = ".".join([sitename,sitetype])
        solrservername = sitetitle
        if sitetype != 'article':
            sitetypemod = sitetype + '.'
            solrserverid = "_".join([sitename,sitetype])
            solrservername = " ".join([sitetitle,sitetype])
        baseUri = sitetypemod + hostname
        # Start configuring sites.
        system("echo ''")
        system("echo ''")
        system("echo 'Enabling and disabling Drupal properties for %s ...'" % sitetitle)
        system("echo ''")
        # Enable modules.
        system("drupal --root=%s --uri=\"http://%s\" module:install  %s --no-interaction" % (drupaldir,baseUri," ".join(modulesToEnable)))
        if installSolr:
            for module in solrModules:
                # Check for search_api_solr_defaults module.
                if module == "search_api_solr_defaults":
                    # Store solr defaults yaml files.
                    system("cp %s/search_api.server.default_solr_server.yml %s/search_api.server.default_solr_server.bak" % (solrconfigpath,solrconfigpath))
                    system("cp %s/search_api.index.default_solr_index.yml %s/search_api.index.default_solr_index.bak" % (solrconfigpath,solrconfigpath))
                    # Update solr defaults yaml settings.
                    set_solr_configs(solrconfigpath,solrserverid,solrservername,solrcorename,solrnew,formavid)
                    # Enable module.
                    system("drupal --root=%s --uri=\"http://%s\" module:install %s --no-interaction" % (drupaldir,baseUri,module))
                    # Restore solr defaults yaml files.
                    system("mv -f %s/search_api.server.default_solr_server.bak %s/search_api.server.default_solr_server.yml" % (solrconfigpath,solrconfigpath))
                    system("mv -f %s/search_api.index.default_solr_index.bak %s/search_api.index.default_solr_index.yml" % (solrconfigpath,solrconfigpath))
                else:
                    # Enable module.
                    system("drupal --root=%s --uri=\"http://%s\" module:install  %s --no-interaction" % (drupaldir,baseUri,module))

        # Install sub-theme.
        system("drupal --root=%s --uri=\"http://%s\" theme:install  %s --set-default" % (drupaldir,baseUri,sitename))
        if installSolr:
            # After all installs disable default search module if solr.
            system("drupal --root=%s --uri=\"http://%s\" module:uninstall  search --no-interaction" % (drupaldir,baseUri))
        # Set configs.
        system("drush -r %s -l http://%s config:set -y block.block.%s_powered status 0 " % (drupaldir,baseUri,sitename))
        # system("drupal --root=%s --uri=\"http://%s\" settings:set  block.block.%s_powered status 0  --no-interaction" % (drupaldir,baseUri,sitename))
        # Clean up.
        system("echo ''")
        system("echo 'Rebuilding %s drupal caches ...'" % baseUri)
        system("drupal --root=%s --uri=\"http://%s\" cache:rebuild" % (drupaldir,baseUri))
        system("echo ''")
        system("echo 'Rebuilding %s drupal content permissions ...'" % baseUri)
        system("drupal --root=%s --uri=\"http://%s\" node:access:rebuild" % (drupaldir,baseUri))
        system("echo ''")
        system("echo 'Finishing setup of drupal files directory for %s ...'" % baseUri)
        # Make private dir and set .htaccess file.
        system("mkdir -p %s/web/sites/%s/files/private" % (drupaldir,baseUri))
        system("echo \"%s\" >  %s/web/sites/%s/files/private/.htaccess" % (HTACCESS,drupaldir,baseUri))
        system("chmod 0444 %s/web/sites/%s/files/private/.htaccess" % (drupaldir,baseUri))
        # Set admin owner all.
        system("chown -R admin:adm %s/web/sites/%s" % (drupaldir,baseUri))
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
        system("drupal --root=%s --uri=\"http://%s\" cron:execute" % (drupaldir,baseUri))
        system("echo ''")
        # Finished drupal setup.
        system("echo 'Please validate %s by viewing the drupal admin status report.'" % baseUri)
        if not os.path.exists("/var/www/admin/images/%s.svg" % sitename):
            system("ln -s %s/web/themes/%s/logo.svg /var/www/admin/images/%s.svg" % (drupaldir,sitename,sitename))
        # Log info.
        logging.info('Drupal site created/configured for %s.' % baseUri)

    # Set admin owner for sites/themes.
    system("chown admin:adm %s/web/sites" % drupaldir)
    system("chown admin:adm %s/web/sites/sites.php" % drupaldir)
    system("chown cssadmin:cssadmin %s/web/themes" % drupaldir)

    # Check formavid logo.
    if not sitename == "formavidorg":
        # Set theme.
        lnTheme = "ln -sf %s/web/themes/%s" % (drupaldir,sitename)
        # Admin Tools - use first "base" site logo.
        lnFile = "logo.svg"
        pathDir = "/var/www/admin/images"
        pathFile = ''.join([pathDir,'/',lnFile])
        if os.path.exists(pathDir) and not os.path.exists(pathFile):
            # Symlink logo to admin pages.
            system("%s/%s %s" % (lnTheme,lnFile,pathFile))

    # Postfix - add virtual addresses.
    system("echo ''")
    system("echo ''")
    system("echo 'Adding %s email addresses to postfix ...'" % hostname)
    system("echo ''")
    system("echo 'webmaster@%s admin' >> /etc/postfix/virtual" % hostname)
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
