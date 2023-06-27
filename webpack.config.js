
module.exports = {
    entry: './myflaskapp/static/scss/main.scss', // Entry point of your SCSS file
    output: {
    filename: 'bundle.js', // Output filename for the compiled JavaScript (not CSS)
    path: __dirname + '/myflaskapp/static/css' // Output directory for the compiled CSS
    },
    mode: 'development', // Set the mode to 'development'
    module: {
    rules: [
    {
    test: /.scss$/,
    use: [
    'style-loader',
    'css-loader',
    'sass-loader'
    ]
    }
    ]
    }
    };