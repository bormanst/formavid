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
<title>User Role Info</title>
</head>
<body>
<h1 align="center">User Role Info</h1>
<div><h3><a href="/structure.php" title="Appliance"><img style="float: left; margin: 0px 15px 0px 0px;" src="images/formavid.png"/><br><br>Appliance</a></h3><br></div>
<div>
<ul>
  <br>
  <li><b>admin:</b> Routine appliance and drupal maintenance.</li>
  <ul>
    <li>System.</li>
    <li>User.</li>
    <li>Apache.</li>
    <li>Dovecot.</li>
    <li>Drupal.</li>
    <li>Fail2ban.</li>
    <li>Postfix.</li>
    <li>Shell-In-A-Box.</li>
    <li>Solr.</li>
    <li>ssh.</li>
    <li>Webmin.</li>
  </ul>
  <br>
  <li><b>cssadmin:</b> Design and related drupal maintenance.</li>
  <ul>
    <li>Theme design privileges.</li>
    <li>Access and permissions to /var/www/drupal7/sites/all/themes directory.</li>
    <li>ProFTPD account mapped to /var/www/drupal7/sites/all/themes directory.</li>
     <li>Access drupal site themes via ftp://admin.HOSTNAME using cssadmin:password account.</li>
    <li>Shell-In-A-Box.</li>
    <li>ssh.</li>
    <li>Compass/Sass:</li>
    <ul>
      <li>Execute watch command from /var/www/drupal7/sites/all/themes directory.</li>
      <li><b>Watch command line:</b> compass watch SITEBASENAME</li>
      <li>Set a compass watch on the site theme directory.</li>
      <li>Edit sass files located within the site's theme sass directory.</li>
      <li>Compass watch should automatically compile changes to the theme css directory.</li>
      <li>View changes to verify before deployment.</li>
      <li>Stop compass watch.</li>
    </ul>
  </ul>
  <br>
  <li><b>drupal7:</b> Drupal database maintenance and scripting.</li>
  <ul>
    <li>Drupal.</li>
    <li>Drush.</li>
  </ul>
  <br>
  <li><b>root (MySQL):</b> Database maintenance and scripting.</li>
  <ul>
    <li>Database maintenance.</li>
    <li>Drush scripts.</li>
    <li>System scripts.</li>
    <li>Drupal.</li>
    <li>Roundup.</li>
    <li>Simple Invoices.</li>
  </ul>
  <br>
  <li><b>root (system):</b> Security and system modifications.</li>
  <ul>
    <li>Login should be left disabled and only be temporarily enabled.</li>
    <li>Enable/disable login as "admin" using Webmin or command line.</li>
    <li>System maintenance requiring root.</li>
    <li>System scripts requiring root.</li>
    <li>Drush.</li>
  </ul>
</ul>
</div>
</body>
</html>
