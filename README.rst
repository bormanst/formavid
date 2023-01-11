The FormaVid Small Business Appliance has been updated for Debian 11 Bullseye:
------------------------------------------------------------------------

- Specifically designed to run on Google Compute Engine's Debian-11 image
  but will run on compatible distros with minor modifications.
- Deployable on local hardware, VMs, or to the cloud.
- Select any compatible base distro and let the scripts do the work.


The FormaVid Small Business Appliance integrates the following features:
------------------------------------------------------------------------


Drupal - Content Management Framework
=======================================

`Drupal`_ is an open source content management platform licensed under
the GPL. Equipped with a powerful blend of features, Drupal can support
a variety of websites ranging from personal blogs, corporate brochures
and large community-driven websites.

- Drupal configurations:

   - Installed from upstream source code to /var/www/drupal9.
   - Includes drush for command line administration and configuration.
   - Includes composer for base component and module administration.
   - Configured to use Gulp/Sass for improved design efficiency.
   - Default theme based upon Zen Grids for mobile first design.
   - Site stacks are created in /var/www/drupal9/prod.
   - Each site stack has its own corresponding apache.conf stack file.

- Additional Drupal modules:

   - Advanced help: Allows developers to store help outside the system.
   - Background Image: Allows utilizing background images.
   - Backup and migrate: Backup and restore your Drupal site
     on-demand or on a schedule.
   - CAPTCHA: A challenge-response test for forms.
   - Chaos tool suite: Set of APIs and tools for developers.
   - Component Libraries: Registers “component libraries” defined by
     your theme or module as Twig namespaces.
   - Devel: A suite of helper modules for Drupal module and theme
     developers.
   - Drush: a command line shell and Unix scripting interface for Drupal.
   - Features: Enables the capture and management of features.
   - Field Group: Enables grouping fields together.
   - FiveStar: Simple five-star voting widget for nodes.
   - Honeypot: Methods for deterring spam bots.
   - Image Style Quality: Allows you to specify a custom quality on
     individual image styles.
   - ImageMagick: Allows to use ImageMagick or GraphicsMagick as image
     toolkit for Image API.
      on the fly resizing.
   - Inline Entity Form: Provides a widget for inline management
     (creation, modification, removal) of referenced entities.
   - Module Filter: The ability to quickly find  modules.
   - Panels: Drag and drop customized layouts for pages, nodes and blocks.
   - PathAuto: Auto-generate search engine friendly URLs (SEO).
   - Recaptcha: Thwart spammers by adding image or text based
     CAPTCHAs to your site.
   - RestUI: Provides a user interface to manage REST resources.
   - Rules: Allows site administrators to define conditionally
     executed actions based on occurring events.
   - Typed Data: Extends the core Typed Data API with new APIs and features.
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

Initial configuration: */etc/roundup/support/tracker-config.ini*

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


Invoice Ninja - Invoicing system
=================================

`Invoice Ninja`_ is a web based invoicing system that is 100% open source, and supported
by a growing community of developers around the world. A suite of features to invoice,
track-time, and to get paid.

- Invoice Ninja configurations:

   - Installed from zip to /var/www/invoiceninja.
   - Setup page is Apache password protected using 'invoiceninja':invoiceninja_password.
   - Apache2 conf file symlinked from /etc/invoiceninja.


Additional Features
-------------------

- SSL support out of the box.
- `Adminer`_ administration frontend for MariaDB (listening on port
  12322 - uses SSL).
- `BorgBackup`_ deduplicating archiver with compression and encryption.
- `Dovecot`_ IMAP/POP3 server (listening on ports 993/143).
- `Fail2ban`_ bans IPs that show malicious signs.
- `OpenSSH`_ SSH server (listening on port 22).
- `Postfix`_ MTA (bound to localhost) to allow sending of email (e.g.,
  password recovery).
- `ProFTPD`_ ftp server (listening on port 21).
- `Webmin`_ (listening on port 12321) with modules for configuring
  Apache2, Dovecot, Fail2ban, PHP, ProFTPD, MariaDB and Postfix.
- `Webshell`_ (listening on port 12320).


Credentials *(passwords required for initialization)*
-------------------------------------------

-  Webmin, Webshell, SSH, MariaDB, Adminer: username **root**
-  Drupal, Roundup: username **admin**
-  Invoice Ninja setup: username **invoiceninja**
-  ProFTPD: username **cssadmin**
-  BorgBackup: repository passphrase

.. _Adminer: https://www.adminer.org/
.. _Apache: https://httpd.apache.org/
.. _BorgBackup: https://www.borgbackup.org/
.. _Dovecot: https://www.dovecot.org/
.. _Drupal: https://www.drupal.org/
.. _Fail2ban: https://www.fail2ban.org/
.. _Invoice Ninja: https://app.invoiceninja.com/invoice_now?rc=p1sk0fldfqful0otedp3haw66i0rlunt
.. _MariaDB: https://mariadb.org/
.. _OpenSSH: https://www.openssh.com/
.. _Postfix: https://www.postfix.org/
.. _ProFTPD: https://www.proftpd.org/
.. _Roundup: https://roundup.sourceforge.net/
.. _Webmin: https://www.webmin.com/
.. _Webshell: https://code.google.com/p/shellinabox/
