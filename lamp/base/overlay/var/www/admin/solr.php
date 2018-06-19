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
<title>Solr Info</title>
</head>
<body>
<h1 align="center">Solr Info</h1>
<div>
  <div style="width: 100%"><h3><img style="float: left; margin: 0px 15px 0px 0px;" src="images/solr.png"/><br><br>Solr Password</h3></div><br>
  <ul>
    <li><b>curl -k --user admin:ADMINPASSWORD http://localhost:8983/solr/admin/authentication -H 'Content-type:application/json' -d '{"set-user": {"admin":"NEWPASSWORD"}}'</li>
    <li><b>curl -k --user admin:ADMINPASSWORD http://localhost:8983/solr/admin/authentication -H 'Content-type:application/json' -d '{"set-user": {"drupal8":"NEWPASSWORD"}}'</li>
    <li><b>Update Drupal 8 Solr entries using using the drupal admin interface.</b></li>
  </ul>
</div>
<br>
</body>
</html>
