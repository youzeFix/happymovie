module.exports = {
    chainWebpack(config){
      //修改htmlWebpackPlugin
      config.plugin('html').tap(args => {
        args[0].title = 'happymovie';
        return args;
      })
    },
    devServer: {
      proxy: {
          '/movie': {
              target: 'http://localhost:5000',
              changeOrigin: true
          },
          '/auth': {
            target: 'http://localhost:5000',
            changeOrigin: true
          },
          '/files': {
            target: 'http://localhost:5000',
            changeOrigin: true
          }
      }
    }
}