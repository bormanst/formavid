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
  <div style="width: 100%"><h3><img style="float: left; margin: 0px 15px 0px 0px;" src="images/solr.png"/><br><br>Solr Password</h3><br></div>
  <ul>
    <li><b>Update /usr/local/solr/server/etc/realm.properties:</b> admin: NEWPASSWORD and drupal7: NEWPASSWORD</li>
    <li><b>Update Drupal Solr entries using a shell command as root (substitute appropriate SITENAME/TLD):</b></li>
    <ul>
      <li>drush -r /var/www/drupal7 --uri=http://SITENAME.TLD solr-set-env-url http://drupal7:NEWPASSWORD@localhost:8983/solr/SITENAME-article</li> 
      <li>drush -r /var/www/drupal7 --uri=http://blog.SITENAME.TLD solr-set-env-url http://drupal7:NEWPASSWORD@localhost:8983/solr/SITENAME-blog</li> 
      <li>drush -r /var/www/drupal7 --uri=http://book.SITENAME.TLD solr-set-env-url http://drupal7:NEWPASSWORD@localhost:8983/solr/SITENAME-book</li> 
      <li>drush -r /var/www/drupal7 --uri=http://forum.SITENAME.TLD solr-set-env-url http://drupal7:NEWPASSWORD@localhost:8983/solr/SITENAME-forum</li> 
      <li>drush -r /var/www/drupal7 --uri=http://poll.SITENAME.TLD solr-set-env-url http://drupal7:NEWPASSWORD@localhost:8983/solr/SITENAME-poll</li> 
    </ul>
  </ul>
</div>
</body>
</html>
