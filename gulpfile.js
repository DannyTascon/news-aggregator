const gulp = require('gulp');
const sass = require('gulp-sass')(require('sass'));


gulp.task('sass', function () {
  return gulp
    .src('myflaskapp/static/scss/**/*.scss')  // Adjust the path if necessary
    .pipe(sass().on('error', sass.logError))
    .pipe(gulp.dest('myflaskapp/static/css'));  // Adjust the path if necessary
});

gulp.task('watch', function () {
  gulp.watch('myflaskapp/static/scss/**/*.scss', gulp.series('sass'));  // Adjust the path if necessary
});

gulp.task('default', gulp.series('sass', 'watch'));

