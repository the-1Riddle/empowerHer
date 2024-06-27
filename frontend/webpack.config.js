const path = require("path");
const MiniCssExtractPlugin = require("mini-css-extract-plugin");
const CssMinimizerPlugin = require("css-minimizer-webpack-plugin");
const TerserPlugin = require("terser-webpack-plugin");
const HtmlWebpackPlugin = require("html-webpack-plugin");
const { CleanWebpackPlugin } = require("clean-webpack-plugin");
const webpack = require("webpack");

const isDevelopment = process.env.NODE_ENV !== "production";


module.exports = {
  mode: isDevelopment ? "development" : "production",
  entry: "./src/index.js",
  output: {
    path: path.resolve(__dirname, "dist"),
    filename: "bundle.js",
  },
  devtool: isDevelopment ? "inline-source-map" : false,
  devServer: {
    port: 3000,
    hot: true, // enable hot module replacement
  },
  module: {
    rules: [
      {
        test: /\.js$/,
        exclude: /node_modules/,
        use: {
          loader: "babel-loader",
        },
      },
      {
        test: /\.scss$/,
        use: [
          isDevelopment ? "style-loader" : MiniCssExtractPlugin.loader,
          "css-loader",
          {
            loader: "postcss-loader",
            options: {
              postcssOptions: {
                plugins: [
                  [
                    "autoprefixer",
                    {
                      grid: true,
                    },
                  ],
                ],
              },
            },
          },
          "sass-loader",
        ],
      },
    ],
    
  },
  plugins: [
    new CleanWebpackPlugin(),
    new HtmlWebpackPlugin({
      template: "./src/index.html",
      filename: "index.html",
    }),
   //new CleanWebpackPlugin(),
    new HtmlWebpackPlugin({
      template: "./src/gender-violence.html",
      filename: "gender-violence.html",
    }),
    new HtmlWebpackPlugin({
      template: "./src/sexual-awareness.html",
      filename: "sexual-awareness.html",
    }),
    new HtmlWebpackPlugin({
      template: "./src/resources.html",
      filename: "resources.html",
    }),
    new HtmlWebpackPlugin({
      template: "./src/wellness.html",
      filename: "wellness.html",
    }),
    new HtmlWebpackPlugin({
      template: "./src/message.html",
      filename: "message.html",
    }),
    isDevelopment && new webpack.HotModuleReplacementPlugin(),
    !isDevelopment &&
      new MiniCssExtractPlugin({
        filename: "[name].[contenthash].css",
      }),
  ].filter(Boolean),
  optimization: {
    minimize: !isDevelopment,
    minimizer: [
      new CssMinimizerPlugin(),
      new TerserPlugin({
        extractComments: false,
      }),
    ],
  },
};