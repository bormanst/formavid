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
      <li>Initial password entered for Drupal admin during appliance install.</li>
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
      <li>Initial password entered for Drupal admin during appliance install.</li>
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
      <li>ssh.</li>
      <li>Webmin.</li>
    </ul>
    <li><b>cssadmin:</b></li>
    <ul>
      <li>Initial password same as entered for Drupal admin during appliance install.</li>
      <li>Theme design privileges.</li>
      <li>Access and permissions to /var/www/drupal9/prod/web/themes directory.</li>
      <li>ProFTPD account mapped to /var/www/drupal9/prod/web/themes directory.</li>
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
      <li>Invoice Ninja.</li>
    </ul>
    <li><b>drupal9:</b></li>
    <ul>
      <li>Initial password same as entered for Drupal admin during appliance install.</li>
      <li>Drupal.</li>
      <li>Drush.</li>
    </ul>
  </ul>
  <div style="width: 100%"><h3><img style="float: left; margin: 0px 15px 0px 0px;" src="images/proftpd.png"/><br><br>ProFTPD</h3></div><br>
  <ul>
    <li><b>cssadmin:</b></li>
    <ul>
      <li>Access drupal site themes via ftp://admin.HOSTNAME using cssadmin:password account.</li>
      <li>Initial password same as entered for Drupal admin during appliance install.</li>
      <li>Theme design privileges.</li>
      <li>Access and permissions to /var/www/drupal9/prod/web/themes directory.</li>
      <li>ProFTPD account mapped to /var/www/drupal9/prod/web/themes directory.</li>
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
  <div style="width: 100%"><h3><img style="float: left; margin: 0px 15px 0px 0px;" src="images/invoiceninja.png"/><br><br>Invoice Ninja</h3></div><br>
  <ul>
    <li>Initial apache password entered for Invoice Ninja setup page occurs during appliance install.</li>
    <li>Special note: application requires <b>user@BASESITENAME.TLD:password</b> for access (email address not just user name.)</li>
    <li>Sign up for a <a href="https://app.invoiceninja.com/invoice_now?rc=p1sk0fldfqful0otedp3haw66i0rlunt" title="Free Cloud Account">Free Cloud Account</a></li>
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
      <li>Initial password entered for Drupal admin during appliance install.</li>
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
