const path =require('path');
const HtmlWebpackPlugin = require("html-webpack-plugin");
module.exports={
  entry:{
    main:'./a.js'
  },
  output:{
    path:path.join(__dirname,'build'),
    publicPath:'/',
    filename:'[name].js',
    clean:true
  },
  mode:'development',
  target:'node',
  module:{
    rules:[{
      test:/\.js$/,
      exclude:/node_modules/,
      loader:"babel-loader",
    }]
  },
  plugins: [
    new HtmlWebpackPlugin({
      template: "./views/index.html"
    })
  ]
}
