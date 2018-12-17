<?php

/**
 * Copyright (C) 2018 Sean Borman <bormanst@gmail.com>.
 * You should have received LICENSE.txt, a copy of the
 * GNU General Public License, along with this program.
 * If not, see <https://www.gnu.org/licenses/>.
 */

namespace Drupal\spy_watch\Plugin\Block;

use Drupal\Core\Access\AccessResult;
use Drupal\Core\Block\BlockBase;
use Drupal\Core\Form\FormStateInterface;
use Drupal\Core\Session\AccountInterface;

/**
 * Provides a Spy Watch block with which you can generate dummy text anywhere.
 *
 * @Block(
 *   id = "spy_watch_block",
 *   admin_label = @Translation("Spy Watch block"),
 * )
 */
class SpyWatchBlock extends BlockBase {

  /**
   * {@inheritdoc}
   */
  public function build() {
    // Return the form @ Form/SpyWatchBlockForm.php.
    return \Drupal::formBuilder()->getForm('Drupal\spy_watch\Form\SpyWatchBlockForm');
  }

  /**
   * {@inheritdoc}
   */
  protected function blockAccess(AccountInterface $account) {
    return AccessResult::allowedIfHasPermission($account, 'set spy watch');
  }

  /**
   * {@inheritdoc}
   */
  public function blockForm($form, FormStateInterface $form_state) {

    $form = parent::blockForm($form, $form_state);

    $config = $this->getConfiguration();

    return $form;
  }

  /**
   * {@inheritdoc}
   */
  public function blockSubmit($form, FormStateInterface $form_state) {
    $this->setConfigurationValue('spy_watch_block_settings', $form_state->getValue('spy_watch_block_settings'));
  }

}
