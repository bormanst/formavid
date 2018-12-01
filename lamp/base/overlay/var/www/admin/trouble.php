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
<title>Trouble Info</title>
</head>
<body>
<h1 align="center">Trouble Info</h1>
<div>
  <div style="width: 100%"><h3><img style="float: left; margin: 0px 15px 0px 0px;" src="images/formavid.png"/><br><br>Can no longer do a task.</h3></div><br>
  <ul>
    <li>Confirm that the exact task acutually worked at some point.</li>
    <li>Address any application/log error messages starting with the ones they both have in common before the rest.</li>
    <li>Check for recent changes/updates to the application/environment.</li>
    <li>Confirm user:group on affected files and chown as required/allowed.</li>
    <li>Confirm permissions on affected files and chmod as required/allowed.</li>
  </ul>
  <div style="width: 100%"><h3><img style="float: left; margin: 0px 15px 0px 0px;" src="images/formavid.png"/><br><br>Adding a new task does not work.</h3></div><br>
  <ul>
    <li>If it is similar to some_similar_task, then see if some_similar_task is working.</li>
    <li>Address any application/log error messages starting with the ones they both have in common before the rest.</li>
    <li>Confirm user:group on affected files make sense or compare to some_similar_task.</li>
    <li>Confirm permissions on affected files make sense or compare to some_similar_task.</li>
    <li>Confirm communication and configuration of network[/apache]/application layers.</li>
    <li>Refer to application documentation.</li>
  </ul>
  <div style="width: 100%"><h3><img style="float: left; margin: 0px 15px 0px 0px;" src="images/formavid.png"/><br><br>Passwords</h3></div><br>
  <ul>
    <li>Passwords are handled by the application, by apache, or sometimes both.</li>
    <li>Refer to the application documentation regarding application password assistance.</li>
    <li>Refer to the <a href="/info.php" title="Info page">Info page local info links</a> for others.</li>
    <li><b>Appliance root password:</b></li>
    <ul>
      <li>Requires direct console/appliance access.</li>
      <li>Appliance uses grub as a bootloader for a Debian based linux distro.</li>
      <li>Refer to online info for a desired method or <a href="http://www.debuntu.org/how-to-recover-root-password-under-linux-with-single-user-mode/" title="How-To: Recover root password under linux with single user mode">how to recover root password</a>.</li>
    </ul>
  </ul>
  <div style="width: 100%"><h3><img style="float: left; margin: 0px 15px 0px 0px;" src="images/formavid.png"/><br><br>Accidentally disabled/deleted all/part of a drupal stack.</h3></div><br>
  <ul>
    <li>/etc/apache2/sites-available/<b>SITEHOSTNAME.conf does exist:</b></li>
    <ul>
      <li>Confirm its contents.</li>
      <li>Confirm its enabled in apache (been symlinked into sites-enabled.)</li>
      <li>Compare /etc/apache2/sites-available/SITEHOSTNAME.conf to the original template /etc/formavid/templates/sites-template/sitehostname.conf.</li>
      <li>Modify and substitute SITEHOSTNAME accordingly.</li>
      <li>Apply/restart apache.</li>
    </ul>
    <li>/etc/apache2/sites-available/<b>SITEHOSTNAME.conf does NOT exist:</b></li>
    <ul>
      <li>Copy /etc/formavid/templates/sites-template/sitehostname.conf into /etc/apache2/sites-available.</li>
      <li>Substitute the desired SITEHOSTNAME for sitehostname in both the file name and the file contents.</li>
      <li>Modify accordingly.</li>
      <li>Add to apache via webmin or symlink into sites-enabled.</li>
      <li>Apply/restart apache.</li>
    </ul>
  </ul>
</div>
<br>
</body>
</html>
