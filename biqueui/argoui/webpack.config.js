const path = require('path');

module.exports = {
  // Other webpack configuration options...
  
  module: {
    rules: [
      // Rule for handling SCSS files
      {
        test: /\.scss$/,
        use: [
          'style-loader',
          'css-loader',
          'sass-loader'
        ],
      },
      
      // Rule for handling font files
      {
        test: /\.(eot|ttf|woff|woff2)$/,
        use: [
          {
            loader: 'file-loader',
            options: {
              outputPath: 'fonts/',
            },
          },
        ],
      },
      
      // Other rules for handling different file types and loaders...
    ],
  },
  
  // Other webpack configuration options...
};
