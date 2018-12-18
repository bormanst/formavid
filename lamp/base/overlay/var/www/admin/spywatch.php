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
<title>Spy Watch Info</title>
</head>
<body>
<h1 align="center">Spy Watch Info</h1>
<div>
  <div style="width: 100%"><h3><img style="float: left; margin: 0px 15px 0px 0px;" src="images/spywatch.png"/><br><br>Spy Watch</h3></div><br>
  <h3>Theme gulp watch state information.</h3>
  <p>Unpack in the <em>modules/custom</em> folder and enable in <strong>/admin/modules</strong>.</p>
  <p>Last, visit <strong>spy_watch/set_watch/state/route/nid</strong> where:</p>
  <ul>
    <li><em>state</em> is the desired gulp <em>watch state</em></li>
    <li><em>route</em> is the <em>current page</em> to return to</li>
    <li><em>nid</em> is the <em>node id</em> of current page if it is content related, otherwise, -1</li>
  </ul>
  <p>There's is a specific <em>spy watch</em> permission that needs to be enabled.</p>
  <h3>Attention</h3>
  <p>Do not forget to disable caching and css aggregation at /admin/config/development/performance while doing theme development or the newly compiled Spy Watch changes may not appear as expected.</p>
  <p>Ocassionlly, a gulp watch will fail on some scss errors. These errors are usually displayed in the terminal and can cause the watch to terminate abnormally leaving the theme in a broken state. Spy Watch does not show the terminal output, so if a theme apears broken, it is recommended to set Spy Watch to another state and then back to the desired state. This will cause gulp to clean out the broken files and regenerate new ones.</p>
  <p>If the theme remains broken, it can be properly debugged using a terminal and executing a gulp watch manually:</p>
  <p>gulp -f /var/www/drupal8/prod/web/themes/{theme to watch}/gulpfile.js watch</p>
  <p>gulp -f /var/www/drupal8/prod/web/themes/{theme to watch}/gulpfile.js watch-scss</p>
  <p>Note: www-data must be the system owner of the entire styleguide directory or Spy Watch will fail. Manually running a gulp watch from the terminal may require temporarily changing the styleguide directory permissions. Please remember to set them back to www-data.</p>
</div>
<br />
</body>
</html>
