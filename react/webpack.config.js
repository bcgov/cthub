const Webpack = require('webpack');
const path = require('path');
const CopyWebpackPlugin = require('copy-webpack-plugin');

const isDevelopment = 'API_BASE' in process.env && process.env.API_BASE === 'http://localhost:8000';

module.exports = {
  devServer: {
    historyApiFallback: true,
    hot: isDevelopment,
    inline: isDevelopment
  },
  devtool: 'source-map',
  resolve: {
    alias: {
      process: 'process/browser',
    },
    fallback: {
      crypto: require.resolve('crypto-browserify'),
      stream: require.resolve('stream-browserify'),
      util: require.resolve('util/'),
    },
  },
  entry: path.resolve(__dirname, 'src', 'index.js'),
  mode: isDevelopment ? 'development' : 'production',
  module: {
    rules: [{
      enforce: 'pre',
      test: /\.js$/,
      use: [{
        loader: 'source-map-loader',
        options: {
          filterSourceMappingUrl: (url, resourcePath) => {
            if (resourcePath.includes('/node_modules/')) {
              return false;
            }

            return true;
          },
        },
      }],
    }, {
      exclude: /node_modules/,
      include: path.resolve(__dirname, 'src'),
      test: /\.(jsx|js)$/,
      use: [{
        loader: 'babel-loader',
        options: {
          presets: [
            ['@babel/preset-env', {
              targets: 'defaults',
            }],
            '@babel/preset-react',
          ],
        },
      }],
    }, {
      test: /\.css$/i,
      use: ['style-loader', 'css-loader'],
    }, {
      test: /\.s[ac]ss$/i,
      use: ['style-loader', 'css-loader', 'sass-loader'],
    }, {
      test: /\.(otf|eot|svg|png|ttf|woff|jpe?g|woff2)$/i,
      use: [{
        loader: 'url-loader',
      }],
    }],
  },
  output: {
    crossOriginLoading: 'anonymous',
    filename: 'static/bundle.js',
    path: path.resolve(__dirname, 'public'),
    publicPath: '/',
  },
  plugins: [
    new Webpack.ProvidePlugin({
      Buffer: ['buffer', 'Buffer'],
      process: 'process/browser',
    }),
    new CopyWebpackPlugin({
      patterns: [{
        from: './src/keycloak-source.json',
        to: './keycloak.json',
        force: true,
        transform(content) {
          const keycloak = JSON.parse(content.toString());

          if ('KEYCLOAK_CLIENT_ID' in process.env) {
            keycloak.resource = process.env.KEYCLOAK_CLIENT_ID;
          }

          if ('KEYCLOAK_REALM' in process.env) {
            keycloak.realm = process.env.KEYCLOAK_REALM;
          }

          if ('KEYCLOAK_URL' in process.env) {
            keycloak['auth-server-url'] = process.env.KEYCLOAK_URL;

            if (process.env.KEYCLOAK_URL === 'http://keycloak:8080/auth/') {
              keycloak['ssl-required'] = 'none';
            }
          }

          return JSON.stringify(keycloak, null, 2);
        },
      }],
    }),
    new Webpack.DefinePlugin({
      __API_BASE__: 'API_BASE' in process.env ? JSON.stringify(process.env.API_BASE) : JSON.stringify('/'),
      __ENABLE_KEYCLOAK__: 'ENABLE_KEYCLOAK' in process.env ? process.env.ENABLE_KEYCLOAK === 'true' : false,
    }),
  ],
};
