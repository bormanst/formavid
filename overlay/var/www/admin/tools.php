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
<title>Tools Info</title>
</head>
<body>
<h1 align="center">Tools Info</h1>
<div>
  <div style="width: 100%"><h3><img style="float: left; margin: 0px 15px 0px 0px;" src="images/formavid.png"/><br><br>Tools Page Locations</h3></div>
  <ul>
    <li><b>Address:</b> https://admin.sedhostname</li>
    <li><b>Pages (php):</b> /var/www/admin</li>
    <li><b>Images:</b> /var/www/admin/images</li>
    <li><b>Security (apache2 authn_dbm):</b> /usr/local/apache2/passwd/admintools/passwords.dbm</li>
    <li><b>Apache configuration:</b> /etc/apache2/sites-available/zzz-admin.sedhostname.conf</li>
    <li><b>CSS (symlinked):</b> /var/www/drupal7/sites/all/themes/sedlowername</li>
  </ul>
  <div style="width: 100%"><h3><img style="float: left; margin: 0px 15px 0px 0px;" src="images/formavid.png"/><br><br>Tools Page Apache Passwords</h3></div>
  <ul>
    <li>This password is also used for the Apache server satus page.</li>
    <li>The password as well as the site access username 'admin' can be changed as desired.</li>
    <li><b>Change tools 'admin' (as sudo/root):</b> htdbm -c /usr/local/apache2/passwd/admintools/passwords.dbm admin</li>
    <li><b>Other users:</b> htdbm -bc /usr/local/apache2/passwd/admintools/passwords.dbm username password</li>
  </ul>
</div>
</body>
</html>
