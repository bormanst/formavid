<?php

/**
 * Copyright (C) 2018 Sean Borman <bormanst@gmail.com>.
 * You should have received LICENSE.txt, a copy of the
 * GNU General Public License, along with this program.
 * If not, see <https://www.gnu.org/licenses/>.
 */

namespace Drupal\spy_watch\Form;

use Drupal\Core\Form\ConfigFormBase;
use Drupal\Core\Form\FormStateInterface;

class SpyWatchForm extends ConfigFormBase {

  /**
   * {@inheritdoc}
   */
  public function getFormId() {
    return 'spy_watch_form';
  }

  /**
   * {@inheritdoc}
   */
  public function buildForm(array $form, FormStateInterface $form_state) {
    // Form constructor.
    $form = parent::buildForm($form, $form_state);
    // Default settings.
    $config = $this->config('spy_watch.settings');

    // Page title field.
    $form['page_title'] = array(
      '#type' => 'textfield',
      '#title' => $this->t('Spy Watch page title:'),
      '#default_value' => $config->get('spy_watch.page_title'),
      '#description' => $this->t('Give your spy watch page a title.'),
    );

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
    $config = $this->config('spy_watch.settings');
    //$config->set('spy_watch.source_text', $form_state->getValue('source_text'));
    $config->set('spy_watch.page_title', $form_state->getValue('page_title'));
    $config->save();
    return parent::submitForm($form, $form_state);
  }

  /**
   * {@inheritdoc}
   */
  protected function getEditableConfigNames() {
    return [
      'spy_watch.settings',
    ];
  }

}
