The FormaVid Small Business Appliance has been completely refactored:
------------------------------------------------------------------------

- Refactored to be a collection of install and configuration scripts.
- No longer incorporates base operating system allowing for user choice.
- Specifically designed to run on Google Compute Engine's Debian-9 image
  but will run on compatible distros with minor modifications.
- All dependencies on other vendor distros have been removed.
- Deployable on local hardware, VMs, or to the cloud.
- Select any compatible base distro and let the scripts do the work.


The FormaVid Small Business Appliance integrates the following features:
------------------------------------------------------------------------


Drupal 8 - Content Management Framework
=======================================

`Drupal`_ is an open source content management platform licensed under
the GPL. Equipped with a powerful blend of features, Drupal can support
a variety of websites ranging from personal blogs, corporate brochures
and large community-driven websites.

- Drupal 8 configurations:

   - Installed from upstream source code to /var/www/drupal8.
   - Includes drush for command line administration and configuration.
   - Includes composer for base component and module administration.
   - Configured to use Gulp/Sass for improved design efficiency.
   - Default theme based upon Zen Grids for mobile first design.
   - Site stacks are created in /var/www/drupal8/sites.
   - Each site stack has its own corresponding apache.conf stack file.

- Additional Drupal 8 modules:

   - Advagg: Advanced CSS/JS Aggregation.
   - Advanced help: Allows developers to store help outside the system.
   - Background Image: Allows utilizing background images.
   - Backup and migrate: Backup and restore your Drupal site
     on-demand or on a schedule.
   - CAPTCHA: A challenge-response test for forms.
   - Component Libraries: Registers “component libraries” defined by
     your theme or module as Twig namespaces.
   - Chaos tool suite: Set of APIs and tools for developers.
   - Devel: A suite of helper modules for Drupal module and theme
     developers.
   - Drush: a command line shell and Unix scripting interface for
     Drupal.
   - Features: Enables the capture and management of features.
   - Field Group: Enables grouping fields together.
   - FiveStar: Simple five-star voting widget for nodes.
   - Honeypot: Methods for deterring spam bots.
   - Image Style Quality: Allows you to specify a custom quality on
     individual image styles.
   - ImageAPI Optimize: allows you to use your preferred toolkit and
     optimize (losslessly) the image when it is saved.
   - ImageMagick: Allows to use ImageMagick or GraphicsMagick as image
     toolkit for Image API.
   - Imce: Powerful image file uploader and browser, with support for
     on the fly resizing.
   - Inline Entity Form: Provides a widget for inline management
     (creation, modification, removal) of referenced entities.
   - Module Filter: The ability to quickly find  modules.
   - Panels: Drag and drop customized layouts for pages, nodes and
     blocks.
   - PathAuto: Auto-generate search engine friendly URLs (SEO).
   - Recaptcha: Thwart spammers by adding image or text based
     CAPTCHAs to your site.
   - Rules: Allows site administrators to define conditionally
     executed actions based on occurring events.
   - Search API Solr Search: Optional customizable search support.
   - Tagadelic: Makes weighted tag clouds from your taxonomy terms.
   - Views Bulk Operations: augments Views by allowing bulk operations
     to be executed on the displayed rows.
   - Zen: a modern, powerful, HTML5 starting theme with component-based
     CSS and a responsive, mobile-first grid design.


Roundup - Issue Tracking System
===============================

`Roundup`_ is a simple-to-use and and powerful issue-tracking system
with command-line, web and e-mail interfaces. Roundup is being used for
bug tracking and TODO list management, issue management, customer help
desk support, and sales lead tracking.

- Roundup configurations:

   - Installed via pip into user`s roundup home folder.
   - Uses Apache2 to serve roundup (instead of roundup-server).
   - Disabled registration confirmation via email (requires mail
     server).
   - Includes Xapian full text indexer (recommended for large issue DB).
   - Includes full timezone support and documentation.
   - Default view hides all issues until user login.

Initial tracker access: https://support.domain/support/
Initial configuration: */etc/roundup/tracker-config.ini*

**Required settings**::

    [tracker]
    web = /                     (before)
    web = https://support.domain/support/  (after)
    # Note: If not set, links in emails will not include server address.

**Recommended settings**::

    [main]
    admin_email = admin
    dispatcher_email = admin
    [mail]
    domain = example.com


SimpleInvoices - Invoicing system
=================================

`SimpleInvoices`_ is a web based invoicing system developed by the
community for the community that helps users create quick and nice
looking invoices without having to set up to much. Install the software,
enter a biller, a customer and go nuts creating invoices!

- SimpleInvoices configurations:

   - Installed from upstream source code to /var/www/simpleinvoices.
   - Apache protected site using 'admin':simpleinvoices_password.
   - Initial user login 'admin@hostname':simpleinvoices_password.


Additional Features
-------------------

- SSL support out of the box.
- `Adminer`_ administration frontend for MariaDB (listening on port
  12322 - uses SSL).
- `Apache Solr`_ optional search server (listening on port 8983).
- `BorgBackup`_ deduplicating archiver with compression and encryption.
- `Dovecot`_ IMAP/POP3 server (listening on ports 993/143).
- `Postfix`_ MTA (bound to localhost) to allow sending of email (e.g.,
  password recovery).
- `ProFTPD`_ ftp server (listening on port 21).
- SSH server (listening on port 22).
- `Webmin`_ (listening on port 12321) with modules for configuring
  Apache2, Dovecot, Fail2ban, PHP, ProFTPD, MariaDB and Postfix.
- `Webshell`_ (listening on port 12320).
- `Fail2ban`_ bans IPs that show malicious signs.


Credentials *(passwords required for initialization)*
-------------------------------------------

-  Webmin, Webshell, SSH, MariaDB, Adminer: username **root**
-  Drupal 8, Roundup, SimpleInvoices: username **admin**
-  ProFTPD: username **cssadmin**
-  BorgBackup: repository passphrase

.. _Adminer: https://www.adminer.org/
.. _Apache: https://httpd.apache.org/
.. _Apache Solr: https://lucene.apache.org/solr/
.. _BorgBackup: https://www.borgbackup.org/
.. _Dovecot: https://www.dovecot.org/
.. _Drupal: https://www.drupal.org/
.. _Fail2ban: https://www.fail2ban.org/
.. _MariaDB: https://mariadb.org/
.. _Postfix: https://www.postfix.org/
.. _ProFTPD: https://www.proftpd.org/
.. _Roundup: https://roundup.sourceforge.net/
.. _SimpleInvoices: https://www.simpleinvoices.org/
.. _Webmin: https://www.webmin.com/
.. _Webshell: https://code.google.com/p/shellinabox/
