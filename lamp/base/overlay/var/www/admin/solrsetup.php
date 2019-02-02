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
<title>Solr Setup</title>
</head>
<body>
<h1 align="center">Solr Setup</h1>
<div>
  <div style="width: 100%"><h3><img style="float: left; margin: 0px 15px 0px 0px;" src="images/solr.png"/><br><br>Solr Setup</h3></div><br>
  <ul>
    <li>As 'root', run /usr/local/formavid/bin/deploy_appliance - set SOLR_INSTALL to True and decide on CREATE_DRUPAL_STACK value.</li>
    <li>Ater solr is enabled, the admin panel should point to the solr admin interface protected by the 'solr admin' password.</li>
    <li>New drupal sites can enable Solr when using the /usr/local/formavid/bin/deploy/python/create-drupal-stack.py script.</li>
    <li>Modify old sites only if Solr needed. See /usr/local/formavid/bin/deploy/python/create-drupal-stack.py for reference.</li>
  </ul>
</div>
<br>
</body>
</html>
