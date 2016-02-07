var gulp = require("gulp"),
    sourcemaps = require("gulp-sourcemaps"),
    concat = require("gulp-concat"),
    less = require('gulp-less'),
    minifyCss = require('gulp-minify-css'),
    uglify = require('gulp-uglifyjs'),
    symlink = require('gulp-sym')
    STATIC = 'studygroup/static';


var LIBS_SCRIPTS = [
    'assets/bower_components/jquery/dist/jquery.js',
    'assets/bower_components/bootstrap/dist/js/bootstrap.js',
    'assets/bower_components/lodash/lodash.min.js',
];

var LIBS_CSS = [
    'assets/bower_components/font-awesome/css/font-awesome.css',
    'assets/bower_components/bootstrap/dist/css/bootstrap.css',
    'assets/css/*.css',
];

var LIBS_FONTS = [
    'assets/bower_components/font-awesome/fonts/**.*',
    'assets/bower_components/bootstrap/fonts/**.*',
    'assets/fonts/*/**.*',
];

gulp.task("fonts", function () {
    return gulp.src(LIBS_FONTS)
        .pipe(gulp.dest(STATIC + '/fonts'));
});

gulp.task("lib-css", function () {
    return gulp.src(LIBS_CSS)
        .pipe(gulp.dest(STATIC + '/dev/css'));
});

gulp.task("lib-js", function () {
    return gulp.src(LIBS_SCRIPTS)
        .pipe(gulp.dest(STATIC + '/dev/js'));
});

gulp.task("js", function () {
    return gulp.src("./assets/js/**/*.js")
        .pipe(sourcemaps.init())
        .pipe(concat("app.js"))
        .pipe(sourcemaps.write("."))
        .pipe(gulp.dest(STATIC + '/dev/js'));
});

gulp.task("img", function () {
    return gulp.src("./frontend/img/*")
        .pipe(gulp.dest(STATIC + '/img'));
});

gulp.task("less", function () {
    return gulp.src('./assets/less/**/*.less')
        .pipe(sourcemaps.init())
        .pipe(less())
        .pipe(sourcemaps.write())
        .pipe(gulp.dest(STATIC + '/dev/css'));
});

gulp.task('minify-css', function () {
    return gulp.src(STATIC + '/dev/css/*.css')
        .pipe(minifyCss({compatibility: 'ie8'}))
        .pipe(concat('style.min.css'))
        .pipe(gulp.dest(STATIC + '/dist'));
});

gulp.task('minify-jslibs', function () {
    return gulp.src(LIBS_SCRIPTS)
        .pipe(uglify())
        .pipe(concat('libs.min.js'))
        .pipe(gulp.dest(STATIC + '/dist'));
});

gulp.task('minify-js', function () {
    return gulp.src(STATIC + '/dev/js/app.js')
        .pipe(uglify())
        .pipe(concat('app.min.js'))
        .pipe(gulp.dest(STATIC + '/dist'));
});

gulp.task('dev-link', function () {
    return gulp.src([STATIC+'/fonts'])
        .pipe(symlink([STATIC+'/dev/fonts']));
});

gulp.task("default", ["js", "less", "img", "fonts", "lib-css", "lib-js", "dev-link"]);

gulp.task('watch', function () {
    gulp.watch('./assets/less/**/*.less', ['less']);
    gulp.watch('./assets/js/**/*.js', ['js']);
    gulp.watch('./assets/img/*', ['img']);
    gulp.watch(LIBS_FONTS, ['fonts']);
    gulp.watch(LIBS_CSS, ['fonts']);
    gulp.watch(LIBS_SCRIPTS, ['fonts']);
});
