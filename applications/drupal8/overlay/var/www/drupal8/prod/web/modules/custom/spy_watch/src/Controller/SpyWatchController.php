<?php

/**
 * Copyright (C) 2018 Sean Borman <bormanst@gmail.com>.
 * You should have received LICENSE.txt, a copy of the
 * GNU General Public License, along with this program.
 * If not, see <https://www.gnu.org/licenses/>.
 */

namespace Drupal\spy_watch\Controller;

use Drupal\Core\Url;
use Drupal\Component\Utility\Html;
use Drupal\Core\Controller\ControllerBase;
use Symfony\Component\HttpFoundation\RedirectResponse;

/**
 * Controller routines for Spy Watch pages.
 */
class SpyWatchController extends ControllerBase {

  /**
   * Sets gulp Watch state.
   * @param string $state
   *   The desired state to set gulp watch.
   *   Watch states: 0:disabled; 1:scss-only; 2:full-watch
   * @param string $route
   *   The original request route to redirect back to.
   * @param string $nid
   *   The original request node id if node entity.
   *   The default of $nid = -1 implies not content page.
   */
  public function set_watch($state, $route, $nid) {

    // Base uri for site for redirects.
    $baseuri = \Drupal::request()->getHost();
    // Signal to use when killing watches.
    $sigterm = 15;
    // Set pattern to remove periods.
    $pattern = '/\./';

    // Initialize watch commands
    $gulpfile = "/var/www/drupal8/prod/web/themes/" . preg_replace($pattern, "", $baseuri) . "/gulpfile.js";
    $watchall = "gulp -f $gulpfile watch > /dev/null 2>&1 &";
    $watchscss = "gulp -f $gulpfile watch-scss > /dev/null 2>&1 &";

    // Initialize watch state.
    $currentstate = 0;

    // Check for full watch.
    $shellex = "pidof 'gulp -f $gulpfile watch'";
    $watchAllPID = trim(shell_exec($shellex));
    if ($watchAllPID) $currentstate = 2;

    // Check for scss only watch.
    $shellex = "pidof 'gulp -f $gulpfile watch-scss'";
    $watchScssPID = trim(shell_exec($shellex));
    if ($watchScssPID) $currentstate = 1;

    // Change watch state based on current state.
    // Switch by requested state and then by current state.
    switch ($state) {
      // Disable.
      case 0:
        switch ($currentstate) {
          // Currently scss-only.
          case 1:
            // Kill scss-only.
            posix_kill($watchScssPID, $sigterm);
            sleep(5);
            break;
          // Currently full-watch.
          case 2:
            // Kill full-watch.
            posix_kill($watchAllPID, $sigterm);
            sleep(5);
            break;
          default:
            break;
        }
        break;
      // Set scss-only.
      case 1:
        switch ($currentstate) {
          // Currently disabled.
          case 0:
            // Set scss-only.
            shell_exec($watchscss);
            sleep(20);
            break;
          // Currently full-watch.
          case 2:
            // Kill full-watch.
            posix_kill($watchAllPID, $sigterm);
            // Set scss-only.
            shell_exec($watchscss);
            sleep(20);
            break;
          default:
            break;
        }
        break;
      // Set full-watch.
      case 2:
        switch ($currentstate) {
          // Currently disabled.
          case 0:
            // Set full-watch.
            shell_exec($watchall);
            sleep(30);
            break;
          // Currently scss-only.
          case 1:
            // Kill scss-only.
            posix_kill($watchScssPID, $sigterm);
            // Set full-watch.
            shell_exec($watchall);
            sleep(30);
            break;
          default:
            break;
        }
        break;
      default:
        break;
    }

    // Verify route.
    $route_provider = \Drupal::service('router.route_provider');
    $exists = count($route_provider->getRoutesByNames([$route])) === 1;

    // Skip redirect if bad route.
    $skip = !$exists;

    // Skip redirect based on route info.
    if (!empty($route)) {
      // Get route object.
      $routeObject = $route_provider->getRouteByName($route);
      // Skip admin routes.
      $skip = \Drupal::service('router.admin_context')->isAdminRoute($routeObject);
      // Skip all node related routes if proper $nid not received.
      if (preg_match('/entity.node.canonical/', $route, $matches) && $nid === -1) $skip = true;
    }

    // Redirect acceptable route.
    if (!$skip) {
        // Redirect using route parameters.
        $route_parameters = [];
        // Redirect using route options.
        $options = ['absolute' => true];
        // Update route parameters accordingly.
        if (preg_match('/entity.node.canonical/', $route, $matches)) {
          // Set node id to original request.
          $route_parameters = ['node' => $nid];
        } else if (preg_match('/entity.user.canonical/', $route, $matches)) {
          // User path so need to get proper id.
          $user = \Drupal\user\Entity\User::load(\Drupal::currentUser()->id());
          // Set user id to original request.
          $route_parameters = ['user' => $user->get('uid')->value];
        }
        // Build url.
        $url = Url::fromRoute($route, $route_parameters, $options);
        // Verify url properly routed.
        if ($url->isRouted()) {
          // Set redirect response to url.
          $response = new RedirectResponse($url->toString());
          // Redirect to url.
          $response->send();
        }
    }

    // Fall through to module page.
    // Get module settings.
    $config = \Drupal::config('spy_watch.settings');
    // Set page title.
    $element['#title'] = Html::escape($config->get('spy_watch.page_title'));
    // Set theme.
    $element['#theme'] = 'spy_watch';
    // Return module page.
    return $element;
  }

}
