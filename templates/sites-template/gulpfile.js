/* eslint-env node, es6 */
/* global Promise */
/* eslint-disable key-spacing, one-var, no-multi-spaces, max-nested-callbacks, quote-props */

// Resources used to create this gulpfile.js:
// - https://github.com/google/web-starter-kit/blob/master/gulpfile.babel.js
// - https://github.com/dlmanning/gulp-sass/blob/master/README.md
// - http://www.browsersync.io/docs/gulp/

// 'use strict';

var importOnce = require('node-sass-import-once'),
  path = require('path');

var del = require('del');

var options = {};

// #############################
// Edit these paths and options.
// #############################

// The root paths are used to construct all the other paths in this
// configuration. The "project" root path is where this gulpfile.js is located.
// While Zen distributes this in the theme root folder, you can also put this
// (and the package.json) in your project's root folder and edit the paths
// accordingly.
options.rootPath = {
  project     : __dirname + '/',
  styleGuide  : __dirname + '/styleguide/',
  theme       : __dirname + '/'
};

options.theme = {
  name       : 'sitethemename',
  root       : options.rootPath.theme,
  components : options.rootPath.theme + 'components/',
  build      : options.rootPath.theme + 'components/asset-builds/',
  css        : options.rootPath.theme + 'components/asset-builds/css/',
  js         : options.rootPath.theme + 'js/'
};

// Set the URL used to access the Drupal website under development. This will
// allow Browser Sync to serve the website and update CSS changes on the fly.
options.drupalURL = 'http://sitehostname';
// options.drupalURL = 'http://localhost';

// Define the node-sass configuration. The includePaths is critical!
options.sass = {
  importer: importOnce,
  includePaths: [
    options.theme.components,
    options.rootPath.project + '../node_modules/breakpoint-sass/stylesheets',
    options.rootPath.project + '../node_modules/chroma-sass/sass',
    options.rootPath.project + '../node_modules/support-for/sass',
    options.rootPath.project + '../node_modules/typey/stylesheets',
    options.rootPath.project + '../node_modules/zen-grids/sass'
  ],
  outputStyle: 'expanded'
};

// Define which browsers to add vendor prefixes for.
// options.autoprefixer = {
//   browsers: [
//     '> 1%',
//     'ie 9'
//   ]
// };

// Define the style guide paths and options.
options.styleGuide = {
  source: [
    options.theme.components
  ],
  mask: /\.less|\.sass|\.scss|\.styl|\.stylus/,
  destination: options.rootPath.styleGuide,

  builder: 'builder/twig',
  namespace: options.theme.name + ':' + options.theme.components,
  'extend-drupal8': true,

  // The css and js paths are URLs, like '/misc/jquery.js'.
  // The following paths are relative to the generated style guide.
  css: [
    // base/special stylesheets
    path.relative(options.rootPath.styleGuide, options.theme.css + 'base.css'),
    path.relative(options.rootPath.styleGuide, options.theme.css + 'layouts.css'),
    path.relative(options.rootPath.styleGuide, options.theme.css + 'chroma-kss-styles.css'),
    path.relative(options.rootPath.styleGuide, options.theme.css + 'kss-only.css'),
    // component stylesheets
    path.relative(options.rootPath.styleGuide, options.theme.css + 'box.css'),
    path.relative(options.rootPath.styleGuide, options.theme.css + 'clearfix.css'),
    path.relative(options.rootPath.styleGuide, options.theme.css + 'comment.css'),
    path.relative(options.rootPath.styleGuide, options.theme.css + 'footer.css'),
    path.relative(options.rootPath.styleGuide, options.theme.css + 'header.css'),
    path.relative(options.rootPath.styleGuide, options.theme.css + 'hidden.css'),
    path.relative(options.rootPath.styleGuide, options.theme.css + 'highlight-mark.css'),
    path.relative(options.rootPath.styleGuide, options.theme.css + 'inline-links.css'),
    path.relative(options.rootPath.styleGuide, options.theme.css + 'inline-sibling.css'),
    path.relative(options.rootPath.styleGuide, options.theme.css + 'messages.css'),
    path.relative(options.rootPath.styleGuide, options.theme.css + 'print-none.css'),
    path.relative(options.rootPath.styleGuide, options.theme.css + 'responsive-video.css'),
    path.relative(options.rootPath.styleGuide, options.theme.css + 'visually-hidden.css'),
    path.relative(options.rootPath.styleGuide, options.theme.css + 'watermark.css'),
    path.relative(options.rootPath.styleGuide, options.theme.css + 'wireframe.css'),
    // form stylesheets
    path.relative(options.rootPath.styleGuide, options.theme.css + 'autocomplete.css'),
    path.relative(options.rootPath.styleGuide, options.theme.css + 'collapsible-fieldset.css'),
    path.relative(options.rootPath.styleGuide, options.theme.css + 'form-item.css'),
    path.relative(options.rootPath.styleGuide, options.theme.css + 'form-table.css'),
    path.relative(options.rootPath.styleGuide, options.theme.css + 'progress-bar.css'),
    path.relative(options.rootPath.styleGuide, options.theme.css + 'progress-throbber.css'),
    path.relative(options.rootPath.styleGuide, options.theme.css + 'resizable-textarea.css'),
    path.relative(options.rootPath.styleGuide, options.theme.css + 'table-drag.css'),
    // navigation stylesheets
    path.relative(options.rootPath.styleGuide, options.theme.css + 'breadcrumb.css'),
    path.relative(options.rootPath.styleGuide, options.theme.css + 'more-link.css'),
    path.relative(options.rootPath.styleGuide, options.theme.css + 'nav-menu.css'),
    path.relative(options.rootPath.styleGuide, options.theme.css + 'navbar.css'),
    path.relative(options.rootPath.styleGuide, options.theme.css + 'pager.css'),
    path.relative(options.rootPath.styleGuide, options.theme.css + 'skip-link.css'),
    path.relative(options.rootPath.styleGuide, options.theme.css + 'tabs.css')
  ],
  js: [
  ],

  homepage: 'homepage.md',
  title: 'sitethemename Style Guide'
};

// Define the paths to the JS files to lint.
options.eslint = {
  files  : [
    options.rootPath.project + 'gulpfile.js',
    options.theme.js + '**/*.js',
    '!' + options.theme.js + '**/*.min.js',
    options.theme.components + '**/*.js',
    '!' + options.theme.build + '**/*.js'
  ]
};

// If your files are on a network share, you may want to turn on polling for
// Gulp watch. Since polling is less efficient, we disable polling by default.
options.gulpWatchOptions = {};
// options.gulpWatchOptions = {interval: 1000, mode: 'poll'};

// Load Gulp and tools we will use.
var gulp      = require('gulp'),
  $           = require('gulp-load-plugins')(),
  browserSync = require('browser-sync').create(),
  // del         = require('del'),
  // gulp-load-plugins will report "undefined" error unless you load gulp-sass manually.
  sass        = require('gulp-sass'),
  gulpIf      = require('gulp-if'),
  kss         = require('kss');

// Define sass files.
var sassFiles = [
  options.theme.components + '**/*.scss',
  // Do not open Sass partials as they will be included as needed.
  '!' + options.theme.components + '**/_*.scss',
  // Chroma markup has its own gulp task.
  '!' + options.theme.components + 'style-guide/kss-example-chroma.scss'
];

// Clean style guide files.
gulp.task('clean:styleguide', function() {
  // You can use multiple globbing patterns as you would with `gulp.src`
  return del([
    options.styleGuide.destination + '*.html',
    options.styleGuide.destination + 'kss-assets',
    options.theme.build + 'twig/*.twig'
  ], {force: true});
});

// Clean CSS files.
gulp.task('clean:css', function() {
  return del([
    options.theme.css + '**/*.css',
    options.theme.css + '**/*.map'
  ], {force: true});
});

// Style guide production.
gulp.task('styles:production', gulp.series('clean:css', function() {
  return gulp.src(sassFiles)
    .pipe(sass(options.sass).on('error', sass.logError))
    .pipe($.autoprefixer(options.autoprefixer))
    .pipe($.rename({dirname: ''}))
    .pipe($.size({showFiles: true}))
    .pipe(gulp.dest(options.theme.css));
}));

// Style guide example.
gulp.task('styleguide:kss-example-chroma', function() {
  return gulp.src(options.theme.components + 'style-guide/kss-example-chroma.scss')
    .pipe(sass(options.sass).on('error', sass.logError))
    .pipe($.replace(/(\/\*|\*\/)\n/g, ''))
    .pipe($.rename('kss-example-chroma.twig'))
    .pipe($.size({showFiles: true}))
    .pipe(gulp.dest(options.theme.build + 'twig'));
});

// Clean style guide and load example.
gulp.task('styleguide', gulp.series('clean:styleguide', 'styleguide:kss-example-chroma', function() {
  return kss(options.styleGuide);
}));

// Debug the generation of the style guide with the --verbose flag.
gulp.task('styleguide:debug', gulp.series('clean:styleguide', 'styleguide:kss-example-chroma', function() {
  options.styleGuide.verbose = true;
  return kss(options.styleGuide);
}));

// Clean all directories.
gulp.task('clean', gulp.parallel('clean:css', 'clean:styleguide'));

// Lint JavaScript.
gulp.task('lint:js', function() {
  return gulp.src(options.eslint.files)
    .pipe($.eslint())
    .pipe($.eslint.format());
});

// Lint JavaScript and throw an error for a CI to catch.
gulp.task('lint:js-with-fail', function() {
  return gulp.src(options.eslint.files)
    .pipe($.eslint())
    .pipe($.eslint.format())
    .pipe($.eslint.failOnError());
});

// Lint Sass.
gulp.task('lint:sass', function() {
  return gulp.src(options.theme.components + '**/*.scss')
    .pipe($.sassLint())
    .pipe($.sassLint.format());
});

// Lint Sass and throw an error for a CI to catch.
gulp.task('lint:sass-with-fail', function() {
  return gulp.src(options.theme.components + '**/*.scss')
    .pipe($.sassLint())
    .pipe($.sassLint.format())
    .pipe($.sassLint.failOnError());
});

// Lint Sass and JavaScript.
gulp.task('lint', gulp.parallel('lint:sass', 'lint:js'));

// Clean Sass.
gulp.task('styles', gulp.series('clean:css', function() {
  return gulp.src(sassFiles)
    .pipe($.sourcemaps.init())
    .pipe(sass(options.sass).on('error', sass.logError))
    .pipe($.autoprefixer(options.autoprefixer))
    .pipe($.rename({dirname: ''}))
    .pipe($.size({showFiles: true}))
    .pipe($.sourcemaps.write('./'))
    .pipe(gulp.dest(options.theme.css))
    .pipe($.if(browserSync.active, browserSync.stream({match: '**/*.css'})));
}));

// Watch for Sass changes and rebuild.
gulp.task('watch:css', gulp.series('lint:sass', 'styles', 'styleguide', function() {
  return gulp.watch(
    options.theme.components + '**/*.scss',
    options.gulpWatchOptions,
    gulp.series('lint:sass', 'styles', 'styleguide'));
}));

// Watch Sass with browser-sync.
gulp.task('browser-sync', gulp.series('watch:css', function() {
  if (!options.drupalURL) {
    return Promise.resolve();
  }
  return browserSync.init({
    proxy: options.drupalURL,
    noOpen: false
  });
}));

// Watch lint Sass with browser-sync.
gulp.task('watch:lint-and-styleguide', gulp.series('lint:sass', 'styleguide', function() {
  return gulp.watch([
    options.theme.components + '**/*.scss',
    options.theme.components + '**/*.twig'
  ], options.gulpWatchOptions, gulp.series('lint:sass', 'styleguide'));
}));

// Watch for JavaScript changes and lint.
gulp.task('watch:js', gulp.series('lint:js', function() {
  return gulp.watch(options.eslint.files, options.gulpWatchOptions, gulp.series('lint:js'));
}));

// Watch for Sass and JavaScript changes.
gulp.task('watch', gulp.parallel('watch:css', 'watch:js'));

// Watch for Sass only changes.
gulp.task('watch-scss', gulp.series('watch:css'));

// Watch for Sass and JavaScript changes with browser sync.
gulp.task('watch:sync', gulp.parallel('browser-sync', 'watch:js'));

// Fix js files.
function isFixed(file) {
  return file.eslint != null && file.eslint.fixed;
}

// Define JavaScript fix options.
options.fix = {
  jsbase: [options.rootPath.theme],
  jscomponents: [
    options.theme.components + '**/*.js',
    '!' + options.theme.build + '**/*.js'
  ],
  jstheme: [
    options.theme.js + '**/*.js',
    '!' + options.theme.js + '**/*.min.js'
  ]
};

// Fix all JavaScript base files.
gulp.task('fix-base-js', function() {
  return gulp
    .src(options.fix.jsbase)
    .pipe($.eslint({fix: true}))
    .pipe($.eslint.format())
    .pipe(gulpIf(isFixed, gulp.dest(options.rootPath.theme)))
    .pipe($.eslint.failOnError());
});

// Fix all JavaScript components files.
gulp.task('fix-components-js', function() {
  return gulp
    .src(options.fix.jscomponents)
    .pipe($.eslint({fix: true}))
    .pipe($.eslint.format())
    .pipe(gulpIf(isFixed, gulp.dest(options.theme.components)))
    .pipe($.eslint.failOnError());
});

// Fix all JavaScript theme files.
gulp.task('fix-theme-js', function() {
  return gulp
    .src(options.fix.jstheme)
    .pipe($.eslint({fix: true}))
    .pipe($.eslint.format())
    .pipe(gulpIf(isFixed, gulp.dest(options.theme.js)))
    .pipe($.eslint.failOnError());
});

// Fix all JavaScript components.
gulp.task('fix-js', gulp.series('fix-base-js', 'fix-components-js', 'fix-theme-js'));

// Build everything.
gulp.task('build', gulp.series('lint', 'styleguide', 'styles:production'));

// The default task.
gulp.task('default', gulp.series('build'));
