<template>
  <div id="app">
    <NavMenuHor/>
    <keep-alive include="movie-library,movie-pick">
      <router-view/>
    </keep-alive>
    <el-divider></el-divider>
    <div style="width:600px;margin:0 auto; padding:20px 0;text-align:center">
      <el-row >
        <el-col :span=14>
          <a target="_blank" href="http://www.beian.gov.cn/portal/registerSystemInfo?recordcode=13010202002976" 
          style="display:inline-block;text-decoration:none;height:20px;line-height:20px;"><img src="./assets/备案图标.png" 
          style="float:left;" alt="备案图标"/>
          <p style="float:left;height:20px;line-height:20px;margin: 0px 0px 0px 5px; color:#939393;">冀公网安备 13010202002976号</p></a>
        </el-col>

        <el-col :span=10>
          <a target="_blank" href="https://beian.miit.gov.cn/" 
          style="display:inline-block;text-decoration:none;height:20px;line-height:20px;">
          <p style="float:left;height:20px;line-height:20px;margin: 0px 0px 0px 5px; color:#939393;">冀ICP备2021026594号-1</p></a>
        </el-col>
      </el-row>
        
        
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
