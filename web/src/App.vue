<template>
  <div id="app">
    <NavMenuHor/>
    <router-view/>
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
  text-align: center;
  color: #2c3e50;
}

body {
  margin:0;
  padding: 0;
}
</style>
