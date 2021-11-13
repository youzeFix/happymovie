<template>
    <div class="pick-result">
        <el-page-header @back="goBack" content="选电影结果页面">
        </el-page-header>
        <!-- <p>{{movie_data}}</p> -->
        
        <el-table
        :data="movie_data"
        highlight-current-row
        style="width: 100%">
        
        <el-table-column
        type="index"
        width="50">
        </el-table-column>

        <el-table-column
        property="name"
        label="电影名称"
        header-align="center">
        </el-table-column>

        <el-table-column
        property="genre"
        label="类型"
        header-align="center"
        :formatter="tableListFormatter">
        </el-table-column>

        <el-table-column
        property="starring"
        label="主演"
        header-align="center"
        :formatter="tableListFormatter">
        </el-table-column>

        <el-table-column
        property="runtime"
        label="电影时长"
        width="80"
        header-align="center">
        </el-table-column>
        <el-table-column
        property="rating"
        label="电影评分"
        width="80"
        header-align="center"
        align="center">
        </el-table-column>
        <el-table-column
        property="likability"
        label="喜爱程度"
        width="80"
        header-align="center"
        align="center">
        </el-table-column>
        <el-table-column
        property="have_seen"
        label="是否看过"
        width="100"
        header-align="center"
        align="center"
        :formatter="haveSeenFormatter">
        </el-table-column>
        <el-table-column
        property="create_time"
        label="创建时间"
        header-align="center"
        width="200"
        align="center">
        </el-table-column>
        <el-table-column
        property="comment"
        label="备注"
        header-align="center"
        align="center"
        >
        </el-table-column>
        </el-table>
    </div>
</template>


<script>
  export default {
      name:'pick-result',
      data() {
        return {
          movie_data: this.$route.params.data
        }
      },
    methods: {
      tableListFormatter(row, column, cellValue){
        if(cellValue){
          return cellValue.join("/")
        }
      },
      haveSeenFormatter(row, column, cellValue){
        if(cellValue == 1){
          return '是'
        }else if(cellValue == 0){
          return '否'
        }
      },
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