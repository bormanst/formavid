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
<title>Appliance Structure Info</title>
</head>
<body>
<h1 align="center">Appliance Structure Info</h1>
<div>
  <div style="width: 100%"><h3><img style="float: left; margin: 0px 15px 0px 0px;" src="images/formavid.png"/><br><br>Appliance</h3></div><br>
  <ul>
    <li><b>Host name:</b> /etc/hostname</li>
    <li><b>Hosts:</b> /etc/hosts</li>
    <li><b>Logs:</b> /var/log</li>
    <li>Compartmentalized Drupal/Solr-core layout allows deployment flexibility:
      <ul>
        <li>Can deploy Solr on different server and use drupal search as backup if lost communication.</li>
        <li>Can deploy drupal stack accross servers (dedicated forum server, etc.)</li>
        <li>Can deploy combination of the above.</li>
      </ul>
    </li>
    <li>Main console screen displays vital information.</li>
    <li>Uses grub boot loader.</li>
  </ul>
</div>
<div>
  <div style="width: 100%"><h3><img style="float: left; margin: 0px 15px 0px 0px;" src="images/formavid.png"/><br><br>Tools</h3></div><br>
  <ul>
    <li><b>Address:</b> https://admin.sedhostname</li>
    <li><b>Location:</b> /var/www/admin</li>
    <li><b>Info:</b> https://admin.sedhostname/tools.php</li>
    <li><b>Security:</b> protected by apache2 authn_dbm</li>
    <li><b>Users:</b> htdbm -bc /usr/local/apache2/passwd/admintools/passwords.dbm username password</li>
    <li><b>php Pages:</b> /var/www/admin</li>
    <li><b>Images:</b> /var/www/admin/images</li>
    <li><b>Header CSS (symlinked):</b> /var/www/drupal8/prod/web/themes/sedlowername</li>
  </ul>
</div>
<div>
  <div style="width: 100%"><h3><img style="float: left; margin: 0px 15px 0px 0px;" src="images/apache.png"/><br><br>Apache</h3></div><br>
  <ul>
    <li><b>Location:</b> /etc/apache2</li>
    <li><b>Logs:</b> /var/log/apache2</li>
    <li>All sites redirected to https by default.</li>
    <li>Webmin module for administration.</li>
  </ul>
</div>
<div>
  <div style="width: 100%"><h3><img style="float: left; margin: 0px 15px 0px 0px;" src="images/dovecot.png"/><br><br>Dovecot</h3></div><br>
  <ul>
    <li><b>Location:</b> /etc/dovecot</li>
    <li><b>Data:</b> /var/lib/dovecot</li>
    <li>Webmin module for administration.</li>
  </ul>
</div>
<div>
  <div style="width: 100%"><h3><img style="float: left; margin: 0px 15px 0px 0px;" src="images/drupal.png"/><br><br>Drupal8</h3></div><br>
  <ul>
    <li><b>Location:</b> /var/www/drupal8</li>
    <li><b>System admin:</b> admin</li>
    <li><b>CSS admin:</b> cssadmin</li>
    <li><b>CSS themes:</b> /var/www/drupal8/prod/web/themes</li>
    <li>Site stacks created using <a href="/drupal.php" title="instructions and script">instructions and script</a>.</li>
    <li>Permanent apache url redirects used to isolate sub sites.</li>
    <li><b>Apache configuration:</b> /etc/apache2/sites-available/HOSTNAME.conf</li>
    <li><b>Base Site (article):</b> http://HOSTNAME</li>
    <li><b>Solr cores (sans aggregator):</b> /var/lib/solr/data/SITENAME</li>
  </ul>
</div>
<div>
  <div style="width: 100%"><h3><img style="float: left; margin: 0px 15px 0px 0px;" src="images/fail2ban.png"/><br><br>Fail2ban</h3></div><br>
  <ul>
    <li><b>Location:</b> /etc/fail2ban</li>
    <li><b>Jails:</b> /etc/fail2ban</li>
    <li><b>Log:</b> /var/log/fail2ban.log</li>
    <li>Webmin module for administration.</li>
  </ul>
</div>
<div>
  <div style="width: 100%"><h3><img style="float: left; margin: 0px 15px 0px 0px;" src="images/postfix.png"/><br><br>Postfix</h3></div><br>
  <ul>
    <li><b>Location:</b> /etc/postfix</li>
    <li><b>Mail (Maildir format):</b> /home/{username}/Maildir</li>
    <li><b>Spool:</b> /var/spool/postfix</li>
    <li><b>Logs:</b> /var/log/mail.*</li>
    <li>Webmin module for administration.</li>
  </ul>
</div>
<div>
  <div style="width: 100%"><h3><img style="float: left; margin: 0px 15px 0px 0px;" src="images/proftpd.png"/><br><br>ProFTPD</h3></div><br>
  <ul>
    <li><b>Location:</b> /etc/proftpd</li>
    <li><b>Server:</b> /srv/ftp</li>
    <li><b>Welcome message:</b> /srv/ftp/welcome.msg</li>
    <li><b>Logs:</b> /var/log/proftpd</li>
    <li>Webmin module for administration.</li>
  </ul>
</div>
<div>
  <div style="width: 100%"><h3><img style="float: left; margin: 0px 15px 0px 0px;" src="images/roundup.png"/><br><br>Roundup</h3></div><br>
  <ul>
    <li><b>Address:</b> https://support.sedhostname/support/</li>
    <li><b>Location:</b> /etc/roundup</li>
    <li><b>Data location:</b> /var/www/support</li>
    <li><b>Tracker configuration:</b> symlink /etc/roundup/tracker-config.ini /var/www/support/config.ini</li>
    <li><b>Apache configuration:</b> symlink /etc/roundup/apache.conf /etc/apache2/sites-available/support.sedhostname.conf</li>
    <li><b>Header CSS:</b> /var/www/drupal8/prod/web/themes/sedlowername</li>
  </ul>
</div>
<div>
  <div style="width: 100%"><h3><img style="float: left; margin: 0px 15px 0px 0px;" src="images/invoiceninja.png"/><br><br>Invoice Ninja</h3></div><br>
  <ul>
    <li><b>Address:</b> https://billing.sedhostname</li>
    <li><b>Location:</b> /var/www/invoiceninja</li>
    <li><b>Apache2 Configuration:</b> /etc/invoiceninja/apache.conf</li>
  </ul>
</div>
<div>
  <div style="width: 100%"><h3><img style="float: left; margin: 0px 15px 0px 0px;" src="images/solr.png"/><br><br>Solr</h3></div><br>
  <ul>
    <li><b>Admin Address:</b> http://sedhostname:8983/solr/#/</li>
    <li><b>Location:</b> /usr/local/solr</li>
    <li><b>Data:</b> /var/lib/solr/data</li>
    <li><b>Password:</b> /var/lib/solr/security.json</li>
    <li><b>Jetty start (Solr):</b> /usr/local/solr/server/start.jar</li>
    <li><b>Jetty configuration:</b> /usr/local/solr/server/etc</li>
    <li><b>Solr configuration:</b> /var/lib/solr/data/solr.xml</li>
    <li><b>Core properties:</b> /var/lib/solr/data/[sitename]/[sitetype]/core.properties</li>
    <li><b>Drupal8 schema:</b> /var/lib/solr/data/[sitename]/[sitetype]/conf/schema.xml</li>
    <li><b>Drupal8 configuration:</b> /var/lib/solr/data/[sitename]/[sitetype]/conf/solrconfig.xml</li>
  </ul>
</div>
<div>
  <div style="width: 100%"><h3><img style="float: left; margin: 0px 15px 0px 0px;" src="images/webmin.png"/><br><br>Webmin</h3></div><br>
  <ul>
    <li><b>Address:</b> https://admin.sedhostname:12321</li>
     <li><b>Location:</b> /etc/webmin</li>
     <li><b>Data:</b> /var/webmin</li>
     <li><b>Log:</b> /var/webmin</li>
  </ul>
</div>
<br>
</body>
</html>
