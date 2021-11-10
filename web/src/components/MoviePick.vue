<template>
<div class="pick-tabs" v-loading="pick_loading">
  <el-tabs class="movie-pick-tabs" v-model="activeTabName" @tab-click="handleClick">
    <el-tab-pane label="按时长" name="time_length_tab">

      <el-row :gutter="10">

      <el-col :span="3">
        <el-input
          type="number"
          placeholder="请输入分钟数"
          v-model="time_length_input"
          min=1>
        </el-input>
      </el-col>
      
        <el-col :span="3">
          <el-select
            v-model="starring_input"
            multiple
            filterable
            allow-create
            default-first-option
            :multiple-limit="5"
            placeholder="请输入主演演员">
            <el-option
              v-for="item in starring_demos"
              :key="item.value"
              :label="item.label"
              :value="item.value">
            </el-option>
          </el-select>
        </el-col>

          <el-col :span="3">
          <el-select
            v-model="genre_input"
            multiple
            filterable
            allow-create
            default-first-option
            :multiple-limit="6"
            placeholder="请输入电影类型">
            <el-option
              v-for="item in genre_demos"
              :key="item.value"
              :label="item.label"
              :value="item.value">
            </el-option>
          </el-select>
          </el-col>

      <el-col :span="3">
        <el-button type="success" @click="timeLengthPickOK()">Pick!</el-button>

      </el-col>
      </el-row>
      
    </el-tab-pane>

    <el-tab-pane label="按部数" name="movies_num_tab">
      <el-row :gutter="10">
      <el-col :span="3">
        <el-input
          type="number"
          placeholder="请输入部数"
          v-model="movies_num_input"
          min=1
          clearable>
        </el-input>
      </el-col>

      <el-col :span="3">
          <el-select
            v-model="starring_input"
            multiple
            filterable
            allow-create
            default-first-option
            :multiple-limit="5"
            placeholder="请输入主演演员">
            <el-option
              v-for="item in starring_demos"
              :key="item.value"
              :label="item.label"
              :value="item.value">
            </el-option>
          </el-select>
        </el-col>

          <el-col :span="3">
          <el-select
            v-model="genre_input"
            multiple
            filterable
            allow-create
            default-first-option
            :multiple-limit="6"
            placeholder="请输入电影类型">
            <el-option
              v-for="item in genre_demos"
              :key="item.value"
              :label="item.label"
              :value="item.value">
            </el-option>
          </el-select>
          </el-col>

      <el-col :span="3">
      <el-button type="success" @click="movieNumsPickOK()">Pick!</el-button>
      </el-col>
      </el-row>
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
        pick_loading: false,
        starring_input:[],
        genre_input:[],
        starring_demos: [{
          value: '刘德华',
          label: '刘德华'
        }, {
          value: '周润发',
          label: '周润发'
        }, {
          value: '肖央',
          label: '肖央'
        }],
        genre_demos: [{
          value: '剧情',
          label: '剧情'
        }, {
          value: '动作',
          label: '动作'
        }, {
          value: '恐怖',
          label: '恐怖'
        }]
      };
    },
    methods: {
      handleClick(tab, event) {
        console.log(tab, event);
      },
      timeLengthPickOK(){
        if(this.time_length_input == 0){
          this.$message({
              showClose: true,
              message: '请输入分钟数',
              type: 'error'
            });
          return
        }
        let that = this;
        this.pick_loading = true;
        this.$axios.post('/movie/pick', {
          'type': 1,
          'data': {
            'value': this.time_length_input,
            'starring': this.starring_input,
            'genre': this.genre_input
          }
        })
        .then(function(response){
          console.log(response.data);
          if(response.data['statusCode'] != -1){
            that.$router.push({name: 'MoviePickResult', params:{data: response.data['data']}})
          }else{
            that.$message({
              showClose: true,
              message: '请输入分钟数',
              type: 'error'
            });
          }
        })
        .catch(function(error){
          console.log(error)
        })
        .then(function(){
          that.pick_loading=false;
        })
      },
      movieNumsPickOK(){
        if(this.movies_num_input == 0){
          this.$message({
              showClose: true,
              message: '请输入部数',
              type: 'error'
            });
          return
        }
        let that = this;
        this.pick_loading = true;
        this.$axios.post('/movie/pick', {
          'type': 2,
          'data': {
            'value': this.movies_num_input,
            'starring': this.starring_input,
            'genre': this.genre_input
          }
        })
        .then(function(response){
          console.log(response.data);
          if(response.data['statusCode'] != -1){
            that.$router.push({name: 'MoviePickResult', params:{data: response.data['data']}})
          }else{
            that.$message({
              showClose: true,
              message: '请输入部数',
              type: 'error'
            });
          }
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