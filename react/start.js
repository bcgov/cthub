const Webpack = require('webpack');
const WebpackDevServer = require('webpack-dev-server');
const path = require('path');

const webpackConfig = require('./webpack.config');

const serverOptions = {
  contentBase: path.join(__dirname, 'public'),
  publicPath: '/',
  index: '/index.html',
  disableHostCheck: true,
  historyApiFallback: {
    verbose: true,
    index: '/index.html',
    rewrites: [{
      from: /\/api/,
      to: '/api',
    }],
  },
  port: 3000,
  compress: true,
  public: 'localhost',
  hot: true,
  watchOptions: {
    ignored: ['node_modules'],
    poll: 1500,
  },
};

WebpackDevServer.addDevServerEntrypoints(webpackConfig, serverOptions);
const compiler = Webpack(webpackConfig);
const devServer = new WebpackDevServer(compiler, serverOptions);

devServer.listen(3000, '0.0.0.0', () => {});
