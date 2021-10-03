<template>
    <div class="pick-result">
        <el-page-header @back="goBack" content="选电影结果页面">
        </el-page-header>
    </div>
</template>


<script>
  export default {
      name:'pick-result',
    methods: {
      goBack() {
        console.log('go back');
        window.history.length > 1 ? this.$router.go(-1) : this.$router.push('/')
      }
    }
  }
</script>

<style scoped>
.pick-result {
    margin-top: 20px;
    margin-left: 10px;
}
</style>