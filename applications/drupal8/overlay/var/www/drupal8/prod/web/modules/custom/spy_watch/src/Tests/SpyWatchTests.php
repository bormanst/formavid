<?php

/**
 * Copyright (C) 2018 Sean Borman <bormanst@gmail.com>.
 * You should have received LICENSE.txt, a copy of the
 * GNU General Public License, along with this program.
 * If not, see <https://www.gnu.org/licenses/>.
 */

namespace Drupal\spy_watch\Tests;

use Drupal\simpletest\WebTestBase;

/**
 * Tests for the Spy Watch module.
 *
 * @group spy_watch
 */
class SpyWatchTests extends WebTestBase {

  /**
   * Modules to install.
   *
   * @var array
   */
  public static $modules = array('spy_watch');

  /**
   * A simple user.
   *
   * @var object
   */
  private $user;

  /**
   * Perform initial setup tasks that run before every test method.
   */
  public function setUp() {
    parent::setUp();
    $this->user = $this->DrupalCreateUser(array(
      'administer site configuration',
      'generate spy watch',
    ));
  }

  /**
   * Tests that the Spy Watch page can be reached.
   */
  public function testSpyWatchPageExists() {
    // Login.
    $this->drupalLogin($this->user);

    // Generator test:
    $this->drupalGet('spy_watch/generate/1/entity.user.canonical/-1');
    $this->assertResponse(200);
  }

  /**
   * Tests the config form.
   */
  public function testConfigForm() {
    // Login.
    $this->drupalLogin($this->user);

    // Access config page.
    $this->drupalGet('admin/config/development/spy_watch');
    $this->assertResponse(200);
    // Test the form elements exist and have defaults.
    $config = $this->config('spy_watch.settings');
    $this->assertFieldByName(
      'page_title',
      $config->get('spy_watch.settings.page_title'),
      'Page title field has the default value'
    );
    $this->assertFieldByName(
      'source_text',
      $config->get('spy_watch.settings.source_text'),
      'Source text field has the default value'
    );

    // Test form submission.
    $this->drupalPostForm(NULL, array(
      'page_title' => 'Test spy watch',
      'source_text' => 'Test spy watch text.',
    ), t('Save configuration'));
    $this->assertText(
      'The configuration options have been saved.',
      'The form was saved correctly.'
    );

    // Test the new values are there.
    $this->drupalGet('admin/config/development/spy_watch');
    $this->assertResponse(200);
    $this->assertFieldByName(
      'page_title',
      'Test spy watch',
      'Page title is OK.'
    );
    $this->assertFieldByName(
      'source_text',
      'Test spy watch text.',
      'Source text is OK.'
    );
  }

}
