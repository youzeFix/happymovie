<template>
<div class="pick-tabs" v-loading="pick_loading">
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
    name: 'movie-pick',
    data() {
      return {
        activeTabName: 'time_length_tab',
        time_length_input: '',
        movies_num_input: '',
        pick_loading: false
      };
    },
    methods: {
      handleClick(tab, event) {
        console.log(tab, event);
      },
      timeLengthPickOK(){
        let that = this;
        this.pick_loading = true;
        this.$axios.post('/movie/pick', {
          'type': 1,
          'value': this.time_length_input
        })
        .then(function(response){
          console.log(response.data);

          that.$router.push({name: 'MoviePickResult', params:{data: response.data['data']}})
        })
        .catch(function(error){
          console.log(error)
        })
        .then(function(){
          that.pick_loading=false;
        })
      },
      movieNumsPickOK(){
        let that = this;
        this.pick_loading = true;
        this.$axios.post('/movie/pick', {
          'type': 2,
          'value': this.movies_num_input
        })
        .then(function(response){
          console.log(response.data);

          that.$router.push({name: 'MoviePickResult', params:{data: response.data['data']}})
        })
        .catch(function(error){
          console.log(error)
        })
        .then(function(){
          that.pick_loading=false;
        })
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