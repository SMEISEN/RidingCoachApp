module.exports = {
  outputDir: 'dist',
  assetsDir: 'static',
  transpileDependencies: [
    'vuetify',
  ],
  publicPath: '',
  devServer: {
    proxy: 'http://localhost:5000',
  },
};
