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
<title>Drupal Sites</title>
</head>
<body>
<h1 align="center">Drupal Sites</h1>
<p>Site stack creation and associated information can be found at <a href="/drupal.php" title="Drupal Local Info">Drupal Local Info</a>. Component sites can be enabled, disabled, or redirected by modifying the corresponding apache configuration file located in the /etc/apache2/sites-available directory. The following links are dynamically generated from the Drupal sites directory and should be active unless intentionally disabled.</p>
<?php
$pattern = '/\./';
$arrBaseSites = array();
$arrFiles = scandir('/var/www/drupal8/prod/web/sites/');
foreach ($arrFiles as $file) if ($file != '.' && $file !='..' && is_dir('/var/www/drupal8/prod/web/sites/' . $file) && count(preg_split($pattern, $file)) == 2) array_push($arrBaseSites, $file);
foreach ($arrBaseSites as $site) {
  $imageName = preg_replace($pattern, "", $site);
  echo "<div><h3><a href='https://",$site,"/user' title='$site'><img style='float: left; margin: 0px 15px 0px 0px; background-color: rgba(0, 0, 0, 0);' src='images/$imageName.svg'/><br>",$site,"</a></h3><ul>";
  foreach ($arrFiles as $file) if (strpos($file, $site) !== false && $file != '.' && $file !='..' && is_dir('/var/www/drupal8/prod/web/sites/' . $file) && count(preg_split($pattern, $file)) > 1 && $file != $site) echo "<li><a href='https://",$file,"/user' title='$file'>",$file,"</a></li><br>";
  echo "</ul></div><br>";
}
?>
</body>
</html>
