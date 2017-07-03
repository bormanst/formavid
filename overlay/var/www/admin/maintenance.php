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
<title>Maintenance Info</title>
</head>
<body>
<h1 align="center">Maintenance Info</h1>
<div>
  <div style="width: 100%"><h3><img style="float: left; margin: 0px 15px 0px 0px;" src="images/formavid.png"/><br><br>Logs</h3></div>
  <ul>
    <li>Check logs occasionally for abnormalities.</li>
  </ul>
</div>
<div>
  <div style="width: 100%"><h3><img style="float: left; margin: 0px 15px 0px 0px;" src="images/formavid.png"/><br><br>Passwords</h3></div>
  <ul>
    <li>Passwords should be changed on a regular basis depending on context and/or usage.</li>
    <li>Change more often if more secure context (e.g. billing users) and/or high usage (e.g. admin site).</li>
    <li>Each application or tool has it's own protection method, see <a href="/info.php" title="Info"><span>Info</span></a> pages for password administration.</li> 
  </ul>
</div>
<div>
  <div style="width: 100%"><h3><img style="float: left; margin: 0px 15px 0px 0px;" src="images/apache.png"/><br><br>Apache</h3></div>
  <ul>
    <li>Check logs occasionally for abnormalities.</li>
  </ul>
</div>
<div>
  <div style="width: 100%"><h3><img style="float: left; margin: 0px 15px 0px 0px;" src="images/dovecot.png"/><br><br>Dovecot</h3></div>
  <ul>
    <li>Check user Maildirs for cleaning/backup on regular basis.</li>
  </ul>
</div>
<div>
  <div style="width: 100%"><h3><img style="float: left; margin: 0px 15px 0px 0px;" src="images/drupal.png"/><br><br>Drupal7</h3></div>
  <ul>
    <li>Check status report for the main site for each stack.</li>
    <li>Update according to report until report is clear. Use drush commnds as needed: <a href="/drupal.php" title="Drupal Info"><span>Drupal Info</span></a>.</li>
    <li>Ensure sites not left in "design compile" mode.</li>
    <li>Ensure database is set to be optimized in cron.</li>
    <li>Ensure backups are functional.</li>
    <li>Ensure space for backups.</li>
  </ul>
</div>
<div>
  <div style="width: 100%"><h3><img style="float: left; margin: 0px 15px 0px 0px;" src="images/fail2ban.png"/><br><br>Fail2ban</h3></div>
  <ul>
    <li>Monitor by having an email sent each day (cron job, etc.).</li>
    <li>Check logs occasionally.</li>
  </ul>
</div>
<div>
  <div style="width: 100%"><h3><img style="float: left; margin: 0px 15px 0px 0px;" src="images/adminer.png"/><br><br>mySQL</h3></div>
  <ul>
    <li>Check logs occasionally for abnormalities.</li>
  </ul>
</div>
<div>
  <div style="width: 100%"><h3><img style="float: left; margin: 0px 15px 0px 0px;" src="images/postfix.png"/><br><br>Postfix</h3></div>
  <ul>
    <li>Check logs on a regular basis.</li>
    <li>Check user Maildirs for cleaning/backup on regular basis.</li>
    <li>Monitor by having some critical system email(s) sent each day (cron job, etc.).</li>
  </ul>
</div>
<div>
  <div style="width: 100%"><h3><img style="float: left; margin: 0px 15px 0px 0px;" src="images/proftpd.png"/><br><br>ProFtpd</h3></div>
  <ul>
    <li>Primary function is to allow sass file transfers by a cssadmin group account.</li>
    <li>If used for other then check user dirs for cleaning/backup on regular basis.</li>
    <li>Check /srv/ftp occasionally for abnormalities.</li>
  </ul>
</div>
<div>
  <div style="width: 100%"><h3><img style="float: left; margin: 0px 15px 0px 0px;" src="images/roundup.png"/><br><br>Roundup</h3></div>
  <ul>
    <li>Ensure backups are functional.</li>
    <li>Ensure space for backups.</li>
  </ul>
</div>
<div>
  <div style="width: 100%"><h3><img style="float: left; margin: 0px 15px 0px 0px;" src="images/simpleinvoices.png"/><br><br>Simple Invoices</h3></div>
  <ul>
    <li>Ensure backups are functional.</li>
    <li>Ensure space for backups.</li>
  </ul>
</div>
<div>
  <div style="width: 100%"><h3><img style="float: left; margin: 0px 15px 0px 0px;" src="images/solr.png"/><br><br>Solr</h3></div>
  <ul>
    <li>Check indexing/cleaning for usage adjustments.</li>
    <li>Ensure cores are not inactive/orphaned after drupal updates.</li>
    <li>Check cores occasionally for abnormalities.</li>
    <li>Check logs occasionally for abnormalities.</li>
  </ul>
</div>
<div>
  <div style="width: 100%"><h3><img style="float: left; margin: 0px 15px 0px 0px;" src="images/webmin.png"/><br><br>Webmin</h3></div>
  <ul>
    <li>Check and apply updates from within Webmin itself.</li>
    <li>Updates appear at bottom of screen for the admin account.</li>
  </ul>
</div>
</body>
</html>
