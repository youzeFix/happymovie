<template>
  <div id="app">
    <NavMenuHor/>
    <keep-alive include="movie-library,movie-pick">
      <router-view/>
    </keep-alive>
    <el-divider></el-divider>
    <div style="width:300px;margin:0 auto; padding:20px 0;">
        <a target="_blank" href="http://www.beian.gov.cn/portal/registerSystemInfo?recordcode=13010202002976" style="display:inline-block;text-decoration:none;height:20px;line-height:20px;"><img src="./assets/备案图标.png" style="float:left;" alt="备案图标"/><p style="float:left;height:20px;line-height:20px;margin: 0px 0px 0px 5px; color:#939393;">冀公网安备 13010202002976号</p></a>
    </div>
  </div>
</template>

<script>
import NavMenuHor from '@/components/NavMenuHor.vue'

export default {
  components: {
    NavMenuHor
  }
}
</script>


<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  /* text-align: center; */
  color: #2c3e50;
}

body {
  margin:0;
  padding: 0;
}
</style>
