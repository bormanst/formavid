<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html lang="en">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<meta http-equiv="Content-Style-Type" content="text/css">
<meta http-equiv="Content-Script-Type" content="text/javascript">
<meta name="MobileOptimized" content="width">
<meta name="HandheldFriendly" content="true">
<meta name="viewport" content="width=device-width">
<meta http-equiv="cleartype" content="on">
<title>User Access Info</title>
</head>
<body>
<h1 align="center">User Access Info</h1>
<div>
  <div><h3><a href="/structure.php" title="Appliance"><img style="float: left; margin: 0px 15px 0px 0px;" src="images/formavid.png"/><br><br>Appliance</a></h3></div><br>
  <ul>
    <li><b>admin:</b></li>
    <ul>
      <li>Initial password entered for Drupal8/Solr admin during appliance install.</li>
      <li>User maintenance.</li>
      <li>System maintenance.</li>
      <li>Apache.</li>
      <li>Composer.</li>
      <li>Dovecot.</li>
      <li>Drupal.</li>
      <li>Drush.</li>
      <li>Fail2ban.</li>
      <li>Postfix.</li>
      <li>Shell-In-A-Box.</li>
      <li>Solr.</li>
      <li>ssh.</li>
      <li>Webmin.</li>
    </ul>
    <li><b>root:</b></li>
    <ul>
      <li>Initial password entered for system root during appliance install.</li>
      <li>Login should be left disabled and only be temporarily enabled.</li>
      <li>Enable/disable login as "admin" using Webmin or command line.</li>
      <li>System maintenance requiring root.</li>
      <li>System scripts requiring root.</li>
      <li>Drush commands.</li>
    </ul>
  </ul>
  <div><h3><a href="/drupal.php" title="Drupal"><img style="float: left; margin: 0px 15px 0px 0px;" src="images/drupal.png"/><br><br>Drupal</a></h3></div><br>
  <ul>
    <li><b>admin:</b></li>
    <ul>
      <li>Initial password entered for Drupal8/Solr admin during appliance install.</li>
      <li>User maintenance.</li>
      <li>System maintenance.</li>
      <li>Apache.</li>
      <li>Composer.</li>
      <li>Dovecot.</li>
      <li>Drupal.</li>
      <li>Drush.</li>
      <li>Fail2ban.</li>
      <li>Postfix.</li>
      <li>Shell-In-A-Box.</li>
      <li>Solr.</li>
      <li>ssh.</li>
      <li>Webmin.</li>
    </ul>
    <li><b>cssadmin:</b></li>
    <ul>
      <li>Initial password same as entered for Drupal7/Solr admin during appliance install.</li>
      <li>Theme design privileges.</li>
      <li>Access and permissions to /var/www/drupal8/themes directory.</li>
      <li>ProFTPD account mapped to /var/www/drupal8/themes directory.</li>
      <li>Access drupal site themes via ftp://admin.HOSTNAME using cssadmin:password account.</li>
      <li>Gulp.</li>
      <li>Shell-In-A-Box.</li>
      <li>ssh.</li>
    </ul>
  </ul>
  <div style="width: 100%"><h3><img style="float: left; margin: 0px 15px 0px 0px;" src="images/adminer.png"/><br><br>MariaDB</h3></div><br>
  <ul>
    <li><b>root:</b></li>
    <ul>
      <li>Initial password entered for MariaDB root during appliance install.</li>
      <li>Database maintenance.</li>
      <li>Database scripts.</li>
      <li>System scripts.</li>
      <li>Composer.</li>
      <li>Drupal.</li>
      <li>Roundup.</li>
      <li>Simple Invoices.</li>
    </ul>
    <li><b>drupal8:</b></li>
    <ul>
      <li>Initial password same as entered for Drupal8/Solr admin during appliance install.</li>
      <li>Drupal.</li>
      <li>Drush.</li>
    </ul>
  </ul>
  <div style="width: 100%"><h3><img style="float: left; margin: 0px 15px 0px 0px;" src="images/proftpd.png"/><br><br>ProFTPD</h3></div><br>
  <ul>
    <li><b>cssadmin:</b></li>
    <ul>
      <li>Access drupal site themes via ftp://admin.HOSTNAME using cssadmin:password account.</li>
      <li>Initial password same as entered for Drupal8/Solr admin during appliance install.</li>
      <li>Theme design privileges.</li>
      <li>Access and permissions to /var/www/drupal8/themes directory.</li>
      <li>ProFTPD account mapped to /var/www/drupal8/themes directory.</li>
    </ul>
  </ul>
  <div style="width: 100%"><h3><img style="float: left; margin: 0px 15px 0px 0px;" src="images/roundup.png"/><br><br>Roundup</h3></div><br>
  <ul>
    <li><b>admin:</b></li>
    <ul>
      <li>Initial password entered for Roundup admin during appliance install.</li>
      <li>Application maintenance.</li>
      <li>User maintenance.</li>
    </ul>
  </ul>
  <div style="width: 100%"><h3><img style="float: left; margin: 0px 15px 0px 0px;" src="images/shell.png"/><br><br>Shell-In-A-Box</h3></div><br>
  <ul>
    <li>admin access.</li>
    <li>cssadmin access.</li>
    <li>root access (when enabled by admin).</li>
  </ul>
  <div><h3><a href="/simpleinvoices.php" title="Simple Invoices"><img style="float: left; margin: 0px 15px 0px 0px;" src="images/simpleinvoices.png"/><br><br>Simple Invoices</a></h3></div><br>
  <ul>
    <li>Initial site and application password entered for Simple Invoices admin during appliance install.</li>
    <li>Special note: application requires <b>admin@BASESITENAME.TLD:password</b> for access (email address not just user name.)</li>
    <li>Site access and initial application account are created with the same password so it is recommended that the passwords are "unsynced" at first opportunity for security reasons.</li>
    <li>Initial apache site access is "admin:password".</li>
    <li>Initial application access is "admin@BASESITENAME.TLD:password".</li>
    <li>Two layer security: need to first access apache site with "admin:sharedpassword" and then the application with "email:userpassword".</li>
  </ul>
  <div><h3><a href="/solr.php" title="Solr"><img style="float: left; margin: 0px 15px 0px 0px;" src="images/solr.png"/><br><br>Solr</a></h3></div><br>
  <ul>
    <li><b>admin:</b></li>
    <ul>
      <li>Initial password entered for Drupal8/Solr admin during appliance install.</li>
      <li>Core maintenance.</li>
      <li>Detailed information.</li>
      <li>Reports.</li>
      <li>Verify drupal dependencies before changes.</li>
    </ul>
  </ul>
  <div><h3><a href="/tools.php" title="Tools"><img style="float: left; margin: 0px 15px 0px 0px;" src="images/formavid.png"/><br><br>Tools</a></h3></div><br>
  <ul>
    <li>Initial password entered for Tools admin during appliance install.</li>
    <li>Initial apache site access is "admin:password".</li>
  </ul>
  <div style="width: 100%"><h3><img style="float: left; margin: 0px 15px 0px 0px;" src="images/webmin.png"/><br><br>Webmin</h3></div><br>
  <ul>
    <li><b>admin:</b></li>
    <ul>
      <li>Initial password entered for Drupal8/Solr admin during appliance install.</li>
      <li>User maintenance.</li>
      <li>System maintenance.</li>
      <li>Apache.</li>
      <li>Composer.</li>
      <li>Dovecot.</li>
      <li>Fail2ban.</li>
      <li>Postfix.</li>
      <li>Shell-In-A-Box access.</li>
      <li>ssh access.</li>
      <li>Webmin access.</li>
      <li>Webmin maintenance.</li>
    </ul>
    <li><b>root:</b></li>
    <ul>
      <li>Login should be left disabled and only be temporarily enabled.</li>
      <li>Enable/disable login as "admin" using Webmin or command line.</li>
    </ul>
  </ul>
</div>
<br>
</body>
</html>
