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
<title>Simple Invoices Info</title>
</head>
<body>
<h1 align="center">Simple Invoices Info</h1>
<div>
  <div style="width: 100%"><h3><img style="float: left; margin: 0px 15px 0px 0px;" src="images/simpleinvoices.png"/><br><br>Simple Invoices Locations</h3><br></div>
  <ul>
    <li><b>Content:</b> /var/www/simpleinvoices</li>
    <li><b>Header:</b> /var/www/simpleinvoices/templates/default/header.tpl</li>
    <li><b>Design templates:</b> /var/www/simpleinvoices/templates/default</li>
    <li><b>Cache (delete files after design changes):</b> /var/www/simpleinvoices/tmp/cache</li>
    <li><b>Database backups:</b> /var/www/simpleinvoices/tmp/database_backups</li>
    <li><b>Logs</b> /var/www/simpleinvoices/tmp/log</li>
  </ul>
  <div style="width: 100%"><h3><img style="float: left; margin: 0px 15px 0px 0px;" src="images/simpleinvoices.png"/><br><br>Simple Invoices Apache Password</h3><br></div>
  <ul>
    <li>Protection from brute force password attacks is provided by the apache/fail2ban mechanism. Therefore, SimpleInvoices requires an apache site access password as well as a SimpleInvoices password.</li>
    <li>The apache site access password defaults to 'admin' and SimpleInvoices password selected during the initial applicance setup.</li>
    <li>The password as well as the site access username 'admin' can be changed as desired.</li>
    <li><b>Change username/password (as sudo/root):</b> htdbm -c /usr/local/apache2/passwd/simpleinvoices/passwords.dbm admin</li>
  </ul>
</div>
</body>
</html>
