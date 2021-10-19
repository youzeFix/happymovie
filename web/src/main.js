import Vue from 'vue'
import App from './App.vue'
import router from './router'
import ElementUI from 'element-ui';
import 'element-ui/lib/theme-chalk/index.css';
import axios from 'axios';
import Vuex from 'vuex'

Vue.use(ElementUI)
Vue.use(Vuex)
Vue.config.productionTip = false
Vue.prototype.$axios = axios

const store = new Vuex.Store({
  state: {
    logged: false
  },
  mutations: {
    logged_in(state){
      state.logged = true
    },
    logged_out(state){
      state.logged = false
    }
  }
})

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')