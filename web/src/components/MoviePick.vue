<template>
<div class="pick-tabs">
  <el-tabs class="movie-pick-tabs" v-model="activeTabName" @tab-click="handleClick">
    <el-tab-pane label="按时长" name="time_length_tab">
      <el-col :span="5">
        <el-input
          type="number"
          placeholder="请输入分钟数"
          v-model="time_length_input"
          min=0>
        </el-input>
      </el-col>
      分钟
      <el-button type="success" @click="timeLengthPickOK()">确认</el-button>
    </el-tab-pane>

    <el-tab-pane label="按部数" name="movies_num_tab">
      <el-col :span="5">
        <el-input
          type="number"
          placeholder="请输入部数"
          v-model="movies_num_input"
          min=0
          clearable>
        </el-input>
      </el-col>
      部
      <el-button type="success" @click="movieNumsPickOK()">确认</el-button>
    </el-tab-pane>
  </el-tabs>
</div>
</template>
<script>
  export default {
    data() {
      return {
        activeTabName: 'time_length_tab',
        time_length_input: '',
        movies_num_input: ''
      };
    },
    methods: {
      handleClick(tab, event) {
        console.log(tab, event);
      },
      timeLengthPickOK(){
        this.$router.push('/pick-result')
      },
      movieNumsPickOK(){
        this.$router.push('/pick-result')
      }
    }
  };
</script>

<style scoped>
.movie-pick-tabs {
    margin-top: 10px;
    margin-left: 20px;
}
</style>