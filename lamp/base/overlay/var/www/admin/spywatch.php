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
  <p>The controller is triggered by <strong>/spy_watch/set_watch/state/route/nid</strong> where:</p>
  <ul>
    <li><em>state</em> is the desired gulp <em>watch state</em></li>
    <li><em>route</em> is the <em>current page</em> to return to</li>
    <li><em>nid</em> is the <em>node id</em> of current page if it is content related, otherwise, -1</li>
  </ul>
  <p>There is a specific <em>spy watch</em> permission that needs to be enabled.</p>
  <p>Lastly, the Spy Watch block will need to be activated at <strong>/admin/structure/block</strong> to access the radio button menu.</p>
  <p>The <strong>Watch All</strong> option is the default gulp watch that catches any changes, including JS files, and rebuilds everything.</p>
  <p>The <strong>Watch SCSS Only</strong> option is a custom gulp watch that catches only SCSS changes. Since it does NOT watch or rebuild everything, it is more responsive to design changes. However, when a session is completed, it is recommended to run a <strong>Watch All</strong> to rebuild everything, especially the style guide.</p>
  <p>Remember to disable watches when theming is finished to avoid wasting cpu resources. They do NOT terminate on their own.</p>
  <p>Also, of note, is that only one <strong>Watch</strong> is active, at any given time, for the selected theme. The controller will disable any current watch prior to activating a new one, including any watches that were started in a terminal. This avoids redundancy that would otherwise waste cpu resources. Watches that are set on other themes are NOT affected.</p>
  <h3>Attention</h3>
  <p>While the placement and formatting of the Spy Watch block is subjective, putting the block in the header section makes it quick and easy to observe while not interfering with the content area layout. The reasoning is that once the header is properly formatted it is usually the least edited section for any given site. Also, the menu only appears for logged in users with the proper permissions so it should not pose an issue to put the block in the header section.</p>
  <p>Do not forget to disable caching and css aggregation at <strong>/admin/config/development/performance</strong> while doing theme development or the newly compiled Spy Watch changes may not appear as expected.</p>
  <p>Ocassionlly, a gulp watch will fail on some scss errors. These errors are usually displayed in the terminal and can cause the watch to terminate abnormally leaving the theme in a broken state. Spy Watch does not show the terminal output, so if a theme apears broken, it is recommended to set Spy Watch to another state and then back to the desired state. This will cause gulp to clean out the broken files and regenerate new ones.</p>
  <p>If the theme remains broken, it can be properly debugged using a terminal and executing a gulp watch manually:</p>
  <p><strong>gulp -f /var/www/drupal8/prod/web/themes/{theme to watch}/gulpfile.js watch</strong></p>
  <p><strong>gulp -f /var/www/drupal8/prod/web/themes/{theme to watch}/gulpfile.js watch-scss</strong></p>
  <p>Note: www-data must be the system owner of the styleguide directory or Spy Watch will fail. Manually running a gulp watch from the terminal may require temporarily changing the styleguide directory permissions. Please remember to set them back to www-data.</p>
</div>
<br />
</body>
</html>
