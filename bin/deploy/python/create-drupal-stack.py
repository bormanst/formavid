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
// ONLY watches for changed scss files, not _scss files.
// Editing of components/base/base.scss, add/delete a space,
// will re-compile some _scss files but not all. Some like
// those in components/init require the normal gulp watch.
// #########################################################
var watch = require('gulp-watch');

gulp.task('watch-scss', ['clean:css'], function () {
  return gulp.src(sassFiles)
    .pipe(watch(sassFiles))
    .pipe(sass(options.sass).on('error', sass.logError))
    .pipe($.autoprefixer(options.autoprefixer))
    .pipe($.rename({dirname: ''}))
    .pipe($.size({showFiles: true}))
    .pipe(gulp.dest(options.theme.css));
});
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
<IfModule mod_php5.c>
  php_flag engine off
</IfModule>

Deny from all
"""
def main():
    try:
        opts, args = getopt.gnu_getopt(sys.argv[1:], "h", ['help', 'apass=', 'dbpass=', 'domain=', 'email=', 'formavid=', 'sitetitle=', 'solr='])
    except getopt.GetoptError, e:
        usage(e)

    # log setup
    logging.basicConfig(filename=DEFAULT_LOG,level=logging.INFO)

    # log start
    logging.info('Start time: %s' % datetime.datetime.now())

    # Get envars.
    dbpass = os.environ.get("DB_PASS")
    domain = os.environ.get("DOMAIN")
    email = os.environ.get("APP_EMAIL")
    formavid = os.environ.get("FORMAVID")
    password = os.environ.get("APP_PASS")
    sitetitle = os.environ.get("SITETITLE")
    solr = os.environ.get("SOLR_INSTALL")

    # check for dbpass
    isdbpass = "DbpasswordEnvar"
    if not dbpass or dbpass == "None": isdbpass = "No-DbpasswordEnvar"

    # check for password
    ispassword = "PasswordEnvar"
    if not password or password == "None": ispassword = "No-PasswordEnvar"

    # log envars
    logging.info('Incoming envars: [isdbpass]:[domain]:[email]:[formavid]:[ispassword]:[sitetitle]:[solr]')
    logging.info('Incoming envars: [%s]:[%s]:[%s]:[%s]:[%s]:[%s]:[%s]' % (isdbpass, domain, email, formavid, ispassword, sitetitle, solr))

    # Assign common dialog header.
    d = Dialog(DEFAULT_DIALOG_HEADER)

    # List of solr related modules.
    solrModules = ['search_api_solr', 'search_api_solr_defaults']
    logging.info('Drupal solr related modules: %s' % solrModules)

    # List of modules to disable.
    modulesToDisable = ['search', 'search_api_solr_defaults']
    logging.info('Drupal modules to disable: %s' % modulesToDisable)

    # List of modules to enable: initially populated by applications/1000-drupal8/drupal8drupal8 script.
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
        elif opt == '--solr':
            solr = val

    # Get formavid location.
    if not formavid or formavid == "None": formavid = "/usr/local/formavid"

    # Get domain.
    if not domain or domain == "None":
        domain = d.get_input(
            "Add Drupal8 Domain",
            "Enter additional domain for Drupal8.",
            DEFAULT_DOMAIN)

    # Preen domain.
    domain = format_domain(domain)

    # Get hostname.
    hostname = get_hostname(domain)

    # Get sitename.
    sitename = get_sitename(domain)

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
        out = system("systemctl is-active solr")
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
            # log issue
            logging.info('You selected Solr search but the solr service is not available!!!')
            quit()
        # Ensure solr related modules in enable list.
        for module in solrModules:
            if module not in modulesToEnable:
                modulesToEnable.append(module)
                system("echo ''")
                system("echo ''")
                system("echo 'The solr related module %s has been appended to the list of modules to enable.'" % module)
                system("echo 'Drush should automatically download %s if it is not locally available.'" % module)
                system("echo 'Ensure that the module %s is syncd with composer.json to prevent updating issues.'" % module)
    else:
        # Remove solr related modules from enable list.
        for module in solrModules:
            if module in modulesToEnable:
                modulesToEnable.remove(module)
        # Update modules to disable list.
        modulesToDisable = []

    if not dbpass or dbpass == "None":
        dbpass = d.get_password(
            "Warning - verify resources exist for additional site.",
            "Please enter password for the MySQL root account.")

    if not password or password == "None":
        password = d.get_password(
            "Warning - verify resources exist for additional site.",
            "Please enter password for the Drupal8 admin account.")

    # log vars
    logging.info('Vars used to create stack: [isdbpass]:[domain]:[email]:[formavid]:[hostname]:[ispassword]:[sitename]:[sitetitle]:[installSolr]')
    logging.info('Vars used to create stack: [%s]:[%s]:[%s]:[%s]:[%s]:[%s]:[%s]:[%s]:[%s]' % (isdbpass, domain, email, formavid, hostname, ispassword, sitename, sitetitle, installSolr))

    # log create start
    logging.info('Starting stack creation: %s' % datetime.datetime.now())

    # Start default site setup.
    system("echo ''")
    system("echo ''")
    system("echo ''")
    system("echo 'Creating default site for %s - this takes a while...'" % hostname)
    system("echo ''")

    # TODO: Add option to specify subdir
    drupalsubdir = "prod"

    # Sites - drupal loaction.
    drupaldir = "/".join(["/var/www/drupal8",drupalsubdir])

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
        system("echo 'Configuring solr search core data...'")
        system("echo ''")
        # Solr - create template dir.
        system("mkdir -p %s/%s" % (templates,sitename))
        for sitetype in siteTypes:
            system("mkdir -p %s/%s/%s" % (templates,sitename,sitetype))
            system("cp -f %s/cores-template/core.properties.template %s/%s/%s/core.properties" % (templates,templates,sitename,sitetype))
            system("sed -i \"s/sedsitename/%s/g\" %s/%s/%s/core.properties" % (sitename,templates,sitename,sitetype))
            system("sed -i \"s/sedsitetype/%s/g\" %s/%s/%s/core.properties" % (sitetype,templates,sitename,sitetype))
        # Solr - load cores.
        solrdata = "/var/lib/solr/data"
        system("mv %s/%s %s" % (templates,sitename,solrdata))
        # Solr - copy drupal solr conf.
        apachesolr = "/".join([drupaldir,"web/modules/contrib/search_api_solr/solr-conf/7.x"])
        for sitetype in siteTypes:
            system("cp -r %s %s/%s/%s/conf" % (apachesolr,solrdata,sitename,sitetype))
        # Solr - ensure owner.
        system("chown -R solr:solr %s/%s" % (solrdata,sitename))
        # Solr - enable changes.
        system("systemctl restart solr")
        system("echo ''")
        system("echo 'Solr search core data configuration is complete.'")
        system("echo ''")
        # log info
        logging.info('Solr search core data configuration is complete.')

    # Hosts - update.
    for sitetype in siteTypes:
        sitetypemod = ''
        if sitetype != 'article':
            sitetypemod = sitetype + '.'
        system("sed -i '/127.0.0.1/s/$/ %s%s/' /etc/hosts" % (sitetypemod,hostname))
        # log info
        logging.info('/etc/hosts configuration is complete.')

    # Sites - prepare templates.
    system("cp -rf %s/sites-template %s/sites-staging" % (templates,templates))

    # Apache - replace sitehostname in confs.
    system("find %s/sites-staging -name \"*.conf\" -exec sed -i \"s/sitehostname/%s/g\" '{}' \\;" % (templates,hostname))

    # Apache - replace drupalsubdir in confs.
    system("find %s/sites-staging -name \"*.conf\" -exec sed -i \"s/drupalsubdir/%s/g\" '{}' \\;" % (templates,drupalsubdir))

    # Apache - add sites available.
    system("cp -f %s/sites-staging/sitehostname.conf /etc/apache2/sites-available/%s.conf" % (templates,hostname))

    # Apache - enable added sites.
    system("cp -sf /etc/apache2/sites-available/%s.conf /etc/apache2/sites-enabled/." % hostname)

    # Set temp owner for sites/themes.
    system("chown root:root %s/web/sites" % drupaldir)
    system("chown root:root %s/web/themes" % drupaldir)

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
        system("echo 'Creating %s drupal site...'" % baseUri)
        system("echo ''")
        system("drupal --root=%s multisite:new  %s http://%s --copy-default --uri=\"http://%s\" --no-interaction" % (drupaldir,baseUri,baseUri,baseUri))
        system("drupal --root=%s --uri=\"http://%s\" site:install:inline --profile=\"standard\" --langcode=\"en\" --db_type=\"mysql\" --db_host=\"127.0.0.1\" --db_name=\"%s_%s\" --db_user=\"admin\" --db_pass=\"%s\" --db_port=\"3306\" --site_name=\"%s\" --site_mail=\"admin@%s\" --account_name=\"admin\" --account_mail=\"admin@%s\" --account_pass=\"%s\" % (drupaldir,baseUri,sitename,sitetype,dbpass,sitetitle,hostname,hostname,password))
        system("chmod 0777 %s/web/sites/%s/files" % (drupaldir,baseUri))
        system("chmod 0444 %s/web/sites/%s/settings.php" % (drupaldir,baseUri))
        # Sites - set trusted_host_patterns.
        esc_baseUri = baseUri.replace(".","\\\\\.")
        new_lines="\$settings['trusted_host_patterns'] = array\(\\n\\t'^" + esc_baseUri + "\$',\\n\);\\n"
        system("sed -i \"/trusted_host_patterns/,/\*\//{n;s|^$|%s|}\" %s/web/sites/%s/settings.php" % (new_lines,drupaldir,hostname))
        # Sites - set private file path.
        system("sed -i \"s/\#\ \$settings\['file_private_path']\ =\ '';/\$settings\['file_private_path']\ =\ 'web\/sites\/%s\/files\/private';/g\" %s/web/sites/%s/settings.php" % (hostname,drupaldir,hostname))
        # Sites - update settings.
        system("echo ''")
        system("echo 'The drupal site %s has been created.'" % baseUri)
        system("echo ''")
        # log info
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
            # log info
            logging.info('Allow perms for drush db access on %s_%s.*.' % (sitename,sitetype))
        # Restart mysql.
        system("echo ''")
        system("echo 'Restarting mysql service...'")
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
    system("echo 'Restarting apache2 service...'")
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
        system("echo 'Rebuilding %s drupal caches...'" % baseUri)
        system("drush -r %s -l http://%s cache-rebuild" % (drupaldir,baseUri))
        system("echo 'Site %s can now be modified.'" % baseUri)

    # Start configuring drupal.
    system("echo ''")
    system("echo ''")
    system("echo 'Creating custom theme for %s based on zen theme...'" % sitetitle)
    system("echo ''")

    # Enable zen sub-theme.
    system("drush -r %s -l http://%s theme:enable -y zen" % (drupaldir,hostname))

    # Create site theme from zen sub-theme.
    system("cp -fpr %s/prod/web/themes/contrib/zen/STARTERKIT %s/prod/web/themes" % (drupaldir,drupaldir))
    system("mv %s/prod/web/themes/STARTERKIT %s/prod/web/themes/%s" % (drupaldir,drupaldir,sitename))
    system("shopt -s globstar")
    system("export REMDIR=`echo $PWD`")
    system("cd %s/prod/web/themes/%s" % (drupaldir,sitename))
    system("rename 's/STARTERKIT/%s/' **" % sitename)
    system("cd $REMDIR")
    system("find %s/prod/web/themes/%s -type f -exec sed -i 's/STARTERKIT/%s/g' {} \;" % (drupaldir,sitename,sitename))

    # Add theme to module list.
    # TODO: need to use theme:enable method here too???
    modulesToEnable.append(sitename)
    system("echo ''")
    system("echo 'Theme for %s is ready for modification.'" % sitetitle)
    system("echo ''")

    # Set local gulp for SASS.
    system("echo ''")
    system("echo 'Setting up local Gulp for %s theme...'" % sitetitle)
    system("sed -i \"s/^[[:space:]]*'use strict';/\/\/\ 'use strict'/g\" %s/web/themes/%s/gulpfile.js" % (drupaldir,sitename))
    system("sed -i \"s/options.drupalURL\ =\ ''\;/options.drupalURL\ =\ 'http:\/\/%s'\;/\" %s/web/themes/%s/gulpfile.js" % (hostname,drupaldir,sitename))
    system("sed -i \"s/node_modules\//..\/node_modules\//g\" %s/web/themes/%s/gulpfile.js" % (drupaldir,sitename))
    system("echo \"%s\" >>  %s/web/themes/%s/gulpfile.js" % (GULP_WATCH_SCSS_SCRIPT,drupaldir,sitename))
    system("echo 'Gulp ready to run locally within theme directory.'")

    # Drupal - set site theme permissions.
    system("chmod -R 0644 %s/web/themes/%s/logo.svg" % (drupaldir,sitename))
    system("chown -R cssadmin:cssadmin %s/web/themes/%s" % (drupaldir,sitename))
    system("chmod -R 775 %s/web/themes/%s" % (drupaldir,sitename))
    system("chown -R www-data:www-data %s/web/themes/%s/styleguide" % (drupaldir,sitename))

    # Set path to solr configs.
    solrconfigpath = "/".join([drupaldir,"modules/contrib/search_api_solr/search_api_solr_defaults/config/optional"])

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
        system("echo 'Enabling and disabling Drupal properties for %s...'" % sitetitle)
        system("echo ''")
        # Enable modules.
        for module in modulesToEnable:
            # Check for search_api_solr_defaults module.
            if module == "search_api_solr_defaults":
                # Store solr defaults yaml files.
                system("cp %s/search_api.server.default_solr_server.yml %s/search_api.server.default_solr_server.bak" % (solrconfigpath,solrconfigpath))
                system("cp %s/search_api.index.default_solr_index.yml %s/search_api.index.default_solr_index.bak" % (solrconfigpath,solrconfigpath))
                # Update solr defaults yaml settings.
                set_solr_configs(solrconfigpath,solrserverid,solrservername,solrcorename,password,formavid)
                # Enable module.
                system("drush -r %s -l http://%s pm-enable -y %s" % (drupaldir,baseUri,module))
                # Restore solr defaults yaml files.
                system("mv -f %s/search_api.server.default_solr_server.bak %s/search_api.server.default_solr_server.yml" % (solrconfigpath,solrconfigpath))
                system("mv -f %s/search_api.index.default_solr_index.bak %s/search_api.index.default_solr_index.yml" % (solrconfigpath,solrconfigpath))
            else:
                # Enable module.
                system("drush -r %s -l http://%s pm-enable -y %s" % (drupaldir,baseUri,module))
        # Disable modules.
        for module in modulesToDisable:
            # Uninstall module - will remain in available module list.
            system("drush -r %s -l http://%s pm-uninstall -y %s" % (drupaldir,baseUri,module))
        # Set configs.
        system("drush -r %s -l http://%s config-set -y system.theme default '%s' " % (drupaldir,baseUri,sitename))
        system("drush -r %s -l http://%s config-set -y block.block.%s_powered status 0 " % (drupaldir,baseUri,sitename))
        # Clean up.
        system("echo ''")
        system("echo 'Rebuilding %s drupal caches...'" % baseUri)
        system("drush -r %s -l http://%s cache-rebuild" % (drupaldir,baseUri))
        system("echo ''")
        system("echo 'Rebuilding %s drupal content permissions...'" % baseUri)
        system("drush -r %s -l http://%s php-eval 'node_access_rebuild();'" % (drupaldir,baseUri))
        system("echo ''")
        system("echo 'Finishing setup of drupal files directory for %s...'" % baseUri)
        system("mkdir %s/web/sites/%s/files/private" % (drupaldir,baseUri))
        system("echo \"%s\" >  %s/web/sites/%s/files/private/.htaccess" % (HTACCESS,drupaldir,baseUri))
        system("chmod 0760 %s/web/sites/%s/files/private" % (drupaldir,baseUri))
        system("chmod 0444 %s/web/sites/%s/files/private/.htaccess" % (drupaldir,baseUri))
        system("chown -R admin:adm %s/web/sites/%s/files" % (drupaldir,baseUri))
        system("chown -R www-data:www-data %s/web/sites/%s/files/css" % (drupaldir,baseUri))
        system("chown -R www-data:www-data %s/web/sites/%s/files/js" % (drupaldir,baseUri))
        system("chown -R www-data:www-data %s/web/sites/%s/files/php" % (drupaldir,baseUri))
        system("echo 'Completed setup of drupal site %s files directory.'" % baseUri)
        system("echo ''")
        system("echo 'Running initial cron job for drupal site %s...'" % baseUri)
        system("drush -r %s -l http://%s cron" % (drupaldir,baseUri))
        system("echo ''")
        system("echo 'Refreshing %s drupal status report...'" % baseUri)
        system("drush -r %s -l http://%s pm-refresh" % (drupaldir,baseUri))
        system("echo ''")
        system("echo 'Please validate %s by viewing the drupal admin status report.'" % baseUri)
        if not os.path.exists("/var/www/admin/images/%s.svg" % sitename):
            system("ln -s %s/web/themes/%s/logo.svg /var/www/admin/images/%s.svg" % (drupaldir,sitename,sitename))
        # log info
        logging.info('Drupal site created/configured for %s.' % baseUri)

    # Reset owner for sites/themes.
    system("chown admin:adm %s/web/sites" % drupaldir)
    system("chown cssadmin:cssadmin %s/web/themes" % drupaldir)

    # Check formavid logo.
    if not sitename == "formavidorg":
        # set theme
        lnTheme = "ln -s %s/web/themes/%s" % (drupaldir,sitename)
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
    system("echo 'Adding %s email addresses to postfix...'" % hostname)
    system("echo ''")
    system("echo 'webmaster@%s admin' >> /etc/postfix/virtual" % hostname)
    system("echo 'admin@%s admin' >> /etc/postfix/virtual" % hostname)
    system("echo 'support@%s admin' >> /etc/postfix/virtual" % hostname)
    # system("systemctl start postfix")
    system("postmap /etc/postfix/virtual")
    # system("systemctl stop postfix")
    system("echo ''")
    system("echo 'Postfix has been updated.'")
    # log info
    logging.info('Postfix has been updated.')

    # End default site setup.
    system("echo ''")
    system("echo ''")
    system("echo 'Default site setup for %s is complete.'" % sitetitle)
    system("echo ''")
    system("echo 'Please validate %s configurations by viewing the drupal admin status reports.'" % sitetitle)
    system("echo ''")
    system("echo ''")

    # log end
    logging.info('Completed stack creation for %s: %s' % (hostname, datetime.datetime.now()))

if __name__ == "__main__":
    main()
