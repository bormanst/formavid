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
<title>Drupal Info</title>
</head>
<body>
<h1 align="center">Drupal Info</h1>
<div>
  <div style="width: 100%"><h3><img style="float: left; margin: 0px 15px 0px 0px;" src="images/drupal.png"/><br><br>Drupal Stack Creation</h3></div><br>
  <ul>
    <li><b>Site stack location:</b> /var/www/drupal9/prod/web/sites</li>
    <li><b>Create stack:</b> /usr/local/foravid/bin/create-drupal-stack.py</li>
    <li>Site stack script must be run as root and requires passwords for 'root':mariadb and 'admin':drupal9.</li>
    <li>Any unused components should be disabled verses uninstalled.</li>
  </ul>
  <div style="width: 100%"><h3><img style="float: left; margin: 0px 15px 0px 0px;" src="images/drupal.png"/><br><br>Disable all/part of a drupal stack.</h3></div><br>
  <ul>
    <li>Noting that nothing loads while apache reloads the stack, optionally put the affected drupal sites in maintenance mode.</li>
    <li><b>Only need to modify/remove</b> the desired drupal stack file <b>SITEHOSTNAME.conf</b> located in /etc/apache2/sites-available and apply/restart apache.</li>
    <li>Affected site <b>files and databases can be left alone</b> unless there are space limitations.</li>
    <li>If modifying/removing an active stack then it is recommended to first back it up with drush or equivalent.</li>
  </ul>
  <div style="width: 100%"><h3><img style="float: left; margin: 0px 15px 0px 0px;" src="images/drupal.png"/><br><br>Common Command Switches</h3></div><br>
  <ul>
    <li><b>Useful drush switches (modify accordingly):</b> -r /var/www/drupal9/prod -l http://sedhostname</li>
    <li><b>Useful composer switches (modify accordingly):</b> -d /var/www/drupal9/prod</li>
    <li><b>Useful dupal console switches (modify accordingly):</b> --root=/var/www/drupal9/prod --uri=http://sedhostname</li>
    <li><b>Note: It is recommended to update Drupal 9 core/modules using Composer instead of drush!</b></li>
    <li><b>Update core/modules using provided composer utility:</b> /var/www/admin/utils/<b>composer_d8up</b></li>
  </ul>
  <div style="width: 100%"><h3><img style="float: left; margin: 0px 15px 0px 0px;" src="images/drupal.png"/><br><br>Drupal Design with cssadmin</h3></div><br>
  <ul>
    <li>Theme design privileges.</li>
    <li>Access and permissions to /var/www/drupal9/prod/web/themes directory.</li>
    <li>ProFTPD account mapped to /var/www/drupal9/prod/web/themes directory.</li>
     <li>Access drupal site themes via ftp://admin.HOSTNAME using cssadmin:password account.</li>
    <li>Shell-In-A-Box.</li>
    <li>ssh.</li>
    <li>Gulp/Sass:</li>
    <ul>
      <li>Execute watch command from /var/www/drupal9/prod/web/themes directory.</li>
      <li><b>Watch command line:</b> gulp watch</li>
      <li>Set a gulp watch with -f flag, i.e gulp watch -f mythemecom/gulpfile.js.</li>
      <li>Edit sass files located within the site's theme directory.</li>
      <li>Gulp watch should automatically compile changes to the components css directory.</li>
      <li>View changes to verify before deployment.</li>
      <li>Stop gulp watch.</li>
    </ul>
  </ul>
</div>
<br>
</body>
</html>
