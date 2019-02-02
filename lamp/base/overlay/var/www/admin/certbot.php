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
<title>Certbot Setup</title>
</head>
<body>
<h1 align="center">Certbot Setup</h1>
<div>
  <div style="width: 100%"><h3><img style="float: left; margin: 0px 15px 0px 0px;" src="images/certbot.png"/><br><br>Certbot Setup</h3></div><br>
  <ul>
    <li>Add entries to DNS and firewalls as needed.</li>
    <li>In /usr/local/formavid/applications/certbot/certbot: modify DOMAINS, HOOKS, METHOD, and WEBROOTS accordingly.</li>
    <li>In /etc/formavid/default_envars: change CERTBOT_INSTALL from "False" to "True".</li>
    <li>As 'root', run /usr/local/formavid/bin/deploy_appliance - set CREATE_DRUPAL_STACK to "False".</li>
    <li>Verify cron job by /var/log/letsencrypt logs.</li>
  </ul>
</div>
<br>
</body>
</html>
