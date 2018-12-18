<!--
* Copyright (C) 2018 Sean Borman <bormanst@gmail.com>.
* You should have received LICENSE.txt, a copy of the
* GNU General Public License, along with this program.
* If not, see <https://www.gnu.org/licenses/>.
-->

Spy Watch
===========

Theme gulp watch state information.

Instructions
------------

Unpack in the *modules/custom* folder (currently in the root of your Drupal 8
installation) and enable in `/admin/modules`.

Then, visit `/admin/config/development/spy_watch` to configure Spy Watch.

Last, visit `/spy_watch/set_watch/state/route/nid` where:
- *state* is the desired gulp watch state
- *route* is the route of current page to return to
- *nid* is the node id of current page if it is content related, otherwise, -1

There's is a specific *spy watch* permission that needs to be enabled.

Attention
---------

Do not forget to disable caching and css aggregation at /admin/config/development/performance while doing theme development or the newly compiled Spy Watch changes may not appear as expected.

Ocassionlly, a gulp watch will fail on some scss errors. These errors are usually displayed in the terminal and can cause the watch to terminate abnormally leaving the theme in a broken state. Spy Watch does not show the terminal output, so if a theme apears broken, it is recommended to set Spy Watch to another state and then back to the desired state. This will cause gulp to clean out the broken files and regenerate new ones.

If the theme remains broken, it can be properly debugged using a terminal and executing a gulp watch manually:

gulp -f /var/www/drupal8/prod/web/themes/{theme to watch}/gulpfile.js watch
gulp -f /var/www/drupal8/prod/web/themes/{theme to watch}/gulpfile.js watch-scss

Note: www-data must be the system owner of the entire styleguide directory or Spy Watch will fail. Manually running a gulp watch from the terminal may require temporarily changing the styleguide directory permissions. Please remember to set them back to www-data.
