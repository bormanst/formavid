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

TODO:

Unpack in the *modules/custom* folder (currently in the root of your Drupal 8
installation) and enable in `/admin/modules`.

Then, visit `/admin/config/development/spy_watch` to configure Spy Watch.

Last, visit `spy_watch/set_watch/state/route/nid` where:
- *state* is the desired gulp watch state
- *route* is the route of current page to return to
- *nid* is the node id of current page if it is content related, otherwise, -1

There's is a specific *spy watch* permission that needs to be enabled.

Attention
---------

Most bugs have been ironed out, holes covered, features added. But this module
is a work in progress. Please report bugs and suggestions, ok?
