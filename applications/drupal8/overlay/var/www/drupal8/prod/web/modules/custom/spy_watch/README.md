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

The controller is triggered by `/spy_watch/set_watch/state/route/nid` where:
- *state* is the desired gulp watch state
- *route* is the route of current page to return to
- *nid* is the node id of current page if it is content related, otherwise, -1

There is a specific *spy watch* permission that needs to be enabled.

Lastly, the Spy Watch block will need to be activated at `/admin/structure/block` to access the radio button menu.

The *Watch All* option is the default gulp watch that catches any changes, including JS files, and rebuilds everything.

The *Watch SCSS Only* option is a custom gulp watch that catches only SCSS changes. Since it does NOT watch or rebuild everything, it is more responsive to design changes. However, when a session is completed, it is recommended to run a *Watch All* to rebuild everything, especially the style guide.

Remember to disable watches when theming is finished to avoid wasting cpu resources. They do NOT terminate on their own.

Also, of note, is that only one *Watch* is active, at any given time, for the selected theme. The controller will disable any current watch prior to activating a new one, including any watches that were started in a terminal. This avoids redundancy that would otherwise waste cpu resources. Watches that are set on other themes are NOT affected.


Attention
---------

While the placement and formatting of the Spy Watch block is subjective, putting the block in the header section makes it quick and easy to observe while not interfering with the content area layout. The reasoning is that once the header is properly formatted it is usually the least edited section for any given site. Also, the menu only appears for logged in users with the proper permissions so it should not pose an issue to put the block in the header section.

Do not forget to disable caching and css aggregation at `/admin/config/development/performance` while doing theme development or the newly compiled Spy Watch changes may not appear as expected.

Occasionally, a gulp watch will fail on some scss errors. These errors are usually displayed in the terminal and can cause the watch to terminate abnormally leaving the theme in a broken state. Spy Watch does not show the terminal output, so if a theme appears broken, it is recommended to set Spy Watch to another state and then back to the desired state. This will cause gulp to clean out the broken files and regenerate new ones.

If the theme remains broken, it can be properly debugged using a terminal and executing a gulp watch manually:

`gulp -f /var/www/drupal8/prod/web/themes/{theme to watch}/gulpfile.js watch`
`gulp -f /var/www/drupal8/prod/web/themes/{theme to watch}/gulpfile.js watch-scss`

Note: www-data must be the system owner of the styleguide directory or Spy Watch will fail. Manually running a gulp watch from the terminal may require temporarily changing the styleguide directory permissions. Please remember to set them back to www-data.
