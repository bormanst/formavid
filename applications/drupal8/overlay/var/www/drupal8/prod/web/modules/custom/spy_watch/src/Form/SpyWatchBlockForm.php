<?php

/**
 * Copyright (C) 2018 Sean Borman <bormanst@gmail.com>.
 * You should have received LICENSE.txt, a copy of the
 * GNU General Public License, along with this program.
 * If not, see <https://www.gnu.org/licenses/>.
 */

namespace Drupal\spy_watch\Form;

use Drupal\Component\Utility\Html;
use Drupal\Core\Form\FormBase;
use Drupal\Core\Form\FormStateInterface;
use Drupal\Core\Url;

/**
 * Spy Watch block form
 */
class SpyWatchBlockForm extends FormBase {

  /**
   * {@inheritdoc}
   */
  public function getFormId() {
    return 'spy_watch_block_form';
  }

  /**
   * {@inheritdoc}
   */
  public function buildForm(array $form, FormStateInterface $form_state) {

    // Get current route.
    $route_name = \Drupal::routeMatch()->getRouteName();
    // Base uri for site for redirects.
    $baseuri = \Drupal::request()->getHost();
    // Set pattern to remove periods.
    $pattern = '/\./';

    // Initialize $current_nid.
    $current_nid = -1;
    // Get current rout node parameters.
    $current_node = \Drupal::routeMatch()->getParameter('node');
    // Verify route is of type node.
    if ($current_node instanceof \Drupal\node\NodeInterface) {
      // Set $current_nid.
      $current_nid = $current_node->id();
    }

    // Watch states.
    // 0:disable/inactive
    // 1:watch-scss (only)
    // 2:watch (all)

    // Set watch state labels.
    $watchOff = "Watch Inactive";
    $watchAll = "Watching All";
    $watchSCSS = "Watching SCSS Only";
    $watchOffState = "Disable Watch";
    $watchAllState = "Watch All (30 second delay)";
    $watchSCSSState = "Watch SCSS Only (15 second delay)";

    // Initialize watch vars.
    $watchState = 0;
    $watchIndicator = "Gray_Light_Icon.svg";
    $watchText = "Watch Inactive";

    // Set gulp file by bae uri.
    $gulpfile = "/var/www/drupal8/prod/web/themes/" . preg_replace($pattern, "", $baseuri) . "/gulpfile.js";

    // Check any watch.
    $shellex = "pidof 'gulp -f $gulpfile watch'";
    $watchAllPID = trim(shell_exec($shellex));
    if ($watchAllPID) {
      // Some watch is active so default to all for now.
      $watchState = 2;
      $watchIndicator = "Green_Light_Icon.svg";
      $watchText = $watchAll;
    }

    // Check scss watch. Overrides any watch.
    $shellex = "pidof 'gulp -f $gulpfile watch-scss'";
    $watchScssPID = trim(shell_exec($shellex));
    if ($watchScssPID) {
      // Detected specific watch-scss so override watch all above.
      $watchState = 1;
      $watchIndicator = "Yellow_Light_Icon.svg";
      $watchText = $watchSCSS;
    }

    // Initialize watchlist form.
    $form['watchlist'] = [
      '#type' => 'details',
      '#title' => t('<b>Set Watch State</b>'),
      '#prefix' => "<br/><img width='14px' height='14px' src='/modules/custom/spy_watch/images-source/$watchIndicator'/>&nbsp;&nbsp;$watchText",
      '#open' => FALSE,
    ];

    // Initialize watchlist state options.
    $options = array(1 => $watchSCSSState, 2 => $watchAllState, 0 => $watchOffState);

    // Update watchlist state options based on current state.
    switch ($watchState) {
      // Watch disabled.
      case 0:
        // Remove off option.
        $options = array(1 => $watchSCSSState, 2 => $watchAllState);
        break;
      // Watch scss-only.
      case 1:
        // Remove scss-only option.
        $options = array(2 => $watchAllState, 0 => $watchOffState);
        break;
      // Watch all.
      case 2:
        // Remove all option.
        $options = array(1 => $watchSCSSState, 0 => $watchOffState);
        break;
    }

    // Set form current watch state.
    $form['watchlist']['watchstate'] = array(
      '#type' => 'radios',
      '#attributes' => array('onchange' => "form.submit('watchlist')"),
      '#options' => $options,
    );

    // Set form current node id.
    $form['watchlist']['nid'] = array(
      '#type' => 'hidden',
      '#value' => $current_nid,
    );

    // Set form current route.
    $form['watchlist']['routename'] = array(
      '#type' => 'hidden',
      '#value' => $route_name,
    );

    // Set form submit values.
    $form['watchlist']['submit'] = array(
      '#type' => 'submit',
      '#value' => 'Submit',
      '#attributes' => array('style' => 'display:none;'),
    );

    // Return updated form.
    return $form;
  }

  /**
   * {@inheritdoc}
   */
  public function validateForm(array &$form, FormStateInterface $form_state) {
  }

  /**
   * {@inheritdoc}
   */
  public function submitForm(array &$form, FormStateInterface $form_state) {

    // Redirect form submission to the appropriate controller.
    $form_state->setRedirect(
      // Redirect to set_watch.
      'spy_watch.set_watch',
      // Set routing values required by set_watch controller.
      array(
        'nid' => $form_state->getValue('nid'),
        'route' => $form_state->getValue('routename'),
        'state' => $form_state->getValue('watchstate'),
      )
    );
  }

}
