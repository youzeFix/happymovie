<template>
<div class="pick-tabs">
  <el-tabs class="movie-pick-tabs" v-model="activeName" @tab-click="handleClick">
    <el-tab-pane label="按时长" name="first">111</el-tab-pane>
    <el-tab-pane label="按部数" name="second">222</el-tab-pane>
  </el-tabs>
</div>
</template>
<script>
  export default {
    data() {
      return {
        activeName: 'second'
      };
    },
    methods: {
      handleClick(tab, event) {
        console.log(tab, event);
      }
    }
  };
</script>

<style scoped>
.movie-pick-tabs {
    margin-top: 10px;
    margin-left: 5px;
}
</style>