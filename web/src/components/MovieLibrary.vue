<template>
    <div class="movie-library">
    <div class="button-group">
        <el-button type="success" icon="el-icon-refresh" @click="loadMovieData()">刷新</el-button>
        <el-button type="primary" icon="el-icon-edit-outline" @click="editMovieData()" :disabled='edit_disabled'>编辑</el-button>
        <el-button @click="setCurrent()">取消选择</el-button>
    </div>
    
    <el-table
        ref="singleTable"
        :data="tableData"
        highlight-current-row
        @current-change="handleCurrentChange"
        style="width: 100%"
        v-loading="loading">
        
        <el-table-column
        type="index"
        width="50">
        </el-table-column>

        <el-table-column
        property="movie_name"
        label="电影名称"
        header-align="center">
        </el-table-column>
        <el-table-column
        property="movie_runtime"
        label="电影时长"
        width="80"
        header-align="center">
        </el-table-column>
        <el-table-column
        property="movie_rating"
        label="电影评分"
        width="80"
        header-align="center"
        align="center">
        </el-table-column>
        <el-table-column
        property="movie_likability"
        label="喜爱程度"
        width="80"
        header-align="center"
        align="center">
        </el-table-column>
        <el-table-column
        property="have_seen"
        label="是否看过"
        width="80"
        header-align="center"
        align="center">
        </el-table-column>
        <el-table-column
        property="create_time"
        label="创建时间"
        header-align="center"
        width="200"
        align="center">
        </el-table-column>
        <el-table-column
        property="origin"
        label="来源"
        header-align="center"
        >
        </el-table-column>
    </el-table>

    <!-- Form -->
    <el-dialog title="编辑电影" :visible.sync="dialogEditFormVisible">
    <el-form :model="movie_form" v-loading="dialogEditLoading">
        <el-form-item label="电影名称">
        <el-input v-model="movie_form.movie_name" autocomplete="off"></el-input>
        </el-form-item>
        <el-form-item label="电影时长">
        <el-input-number v-model="movie_form.movie_runtime" controls-position="right" :min="1" :max="1000"></el-input-number>
        分钟
        </el-form-item>

        <el-form-item label="电影评分">
        <el-input-number v-model="movie_form.movie_rating" controls-position="right" :precision="1" :step="0.1" :min="0" :max="10"></el-input-number>
        </el-form-item>

        <el-form-item label="喜爱程度">
        <el-input-number v-model="movie_form.movie_likability" controls-position="right" :min="0" :max="10"></el-input-number>
        </el-form-item>

        <el-form-item label="是否看过">
        <el-switch v-model="movie_form.have_seen"></el-switch>
        </el-form-item>

        <el-form-item label="创建时间">
        <el-date-picker
        v-model="movie_form.create_time"
        type="datetime"
        placeholder="选择日期时间">
        </el-date-picker>
        </el-form-item>

        <el-form-item label="来源">
        <el-input type="textarea" v-model="movie_form.origin"></el-input>
        </el-form-item>
    </el-form>
    <div slot="footer" class="dialog-footer">
        <el-button @click="dialogEditFormVisible = false">取 消</el-button>
        <el-button type="primary" @click="editDialogOk()">确 定</el-button>
    </div>
    </el-dialog>


    <el-dialog title="新增电影" :visible.sync="dialogAddFormVisible">
    <el-form :model="movie_form">
        <el-form-item label="电影名称">
        <el-input v-model="movie_form.movie_name" autocomplete="off"></el-input>
        </el-form-item>
        <el-form-item label="电影时长">
        <el-input-number v-model="movie_form.movie_runtime" controls-position="right" :min="1" :max="1000"></el-input-number>
        分钟
        </el-form-item>

        <el-form-item label="电影评分">
        <el-input-number v-model="movie_form.movie_rating" controls-position="right" :precision="1" :step="0.1" :min="0" :max="10"></el-input-number>
        </el-form-item>

        <el-form-item label="喜爱程度">
        <el-input-number v-model="movie_form.movie_likability" controls-position="right" :min="0" :max="10"></el-input-number>
        </el-form-item>

        <el-form-item label="是否看过">
        <el-switch v-model="movie_form.have_seen"></el-switch>
        </el-form-item>

        <el-form-item label="创建时间">
        <el-date-picker
        v-model="movie_form.create_time"
        type="datetime"
        placeholder="选择日期时间">
        </el-date-picker>
        </el-form-item>

        <el-form-item label="来源">
        <el-input type="textarea" v-model="movie_form.origin"></el-input>
        </el-form-item>
    </el-form>
    <div slot="footer" class="dialog-footer">
        <el-button @click="dialogAddFormVisible = false">取 消</el-button>
        <el-button type="primary" @click="dialogAddFormVisible = false">确 定</el-button>
    </div>
    </el-dialog>
    
    </div>
</template>

<script>
  export default {
    data() {
      return {
        tableData: [],
        currentRow: null,
        loading: false,
        edit_disabled: true,
        dialogEditFormVisible: false,
        dialogAddFormVisible: false,
        movie_form: {
            movie_id: 0,
            movie_name: '',
            movie_runtime: '',
            movie_rating: '',
            movie_likability: '',
            have_seen: '',
            create_time: '',
            origin: ''
        },
        dialogEditLoading: false
      }
    },

    methods: {
      setCurrent(row) {
        this.$refs.singleTable.setCurrentRow(row);
        if(!row){
            this.edit_disabled=true;
        }
      },
      handleCurrentChange(val) {
        this.currentRow = val;
        this.edit_disabled=false;
      },
      loadMovieData(){
        this.loading=true
        let that = this;
        this.$axios.get('/movie/all')
        .then(function (response){
            that.tableData = response.data;
        })
        .catch(function (error){
            console.log(error);
        })
        .then(function(){
            that.loading=false;
        });
      },
      isDeepObjectEqual(obj1, obj2) {

        //1.如果是比较对象===，返回true
        if (obj1 === obj2) return true;

        //2.如果比较的是两个方法，转成字符串比较
        if (typeof obj1 === "function" && typeof obj2 === "function") return obj1.toString() === obj2.toString();

        //3如果obj1和obj2都是Date实例，获取毫秒值比较
        if (obj1 instanceof Date && obj2 instanceof Date) return obj1.getTime() === obj2.getTime();

        //4如果比较是两个类型不一致,无须比较直接返回false
        if ( Object.prototype.toString.call(obj1) !==Object.prototype.toString.call(obj2) || typeof obj1 !== "object") return false;
        
        //5.获取对象所有自身属性的属性名（包括不可枚举属性但不包括Symbol值作为名称的属性
        const obj1Props = Object.getOwnPropertyNames(obj1);
        const obj2Props = Object.getOwnPropertyNames(obj2);

        //自身属性长度相等,
        if(obj1Props.length !== obj2Props.length) return false;

        //递归调用判断每一个属性值是否相等
        return (obj1Props.every(prop => this.isDeepObjectEqual(obj1[prop], obj2[prop])));
      },
      editMovieData(){
          console.log(this.currentRow);
          this.movie_form.movie_id = this.currentRow.index;
          this.movie_form.movie_name = this.currentRow.movie_name;
          this.movie_form.movie_runtime = this.currentRow.movie_runtime.match(/(\d+)分钟/)[1];
          this.movie_form.movie_rating = this.currentRow.movie_rating;
          this.movie_form.movie_likability = this.currentRow.movie_likability;
          this.movie_form.have_seen = this.currentRow.have_seen;
          this.movie_form.create_time = this.currentRow.create_time;
          this.movie_form.origin = this.currentRow.origin;
          this.movie_copy = Object.assign({}, this.movie_form);
          this.dialogEditFormVisible = true;
      },
      editDialogOk(){
        if(!this.isDeepObjectEqual(this.movie_copy, this.movie_form)){
          console.log('movie_form is changed');
          let prop_diff = {};
          for(let prop in this.movie_copy){
            if(this.movie_copy[prop] != this.movie_form[prop]){
              prop_diff[prop]=this.movie_form[prop];
            }
          }
          if(Object.keys(prop_diff).length){
            prop_diff['id'] = this.movie_copy.movie_id;
            const headerJSON = {
                "Content-Type": "application/json"
            };
            console.log(this.movie_copy)
            let that = this;
            this.dialogEditLoading = true;
            this.$axios.put('/movie/', prop_diff, {headers:headerJSON})
            .then(function(response){
              console.log('update success'+response.data);
              that.dialogEditFormVisible = false;
            })
            .catch(function(error){
              console.log(error);
            })
            .then(function(){
              that.dialogEditLoading=false;
            })
          }
        }else{
          console.log('movie not change'+this.movie_form.movie_likability+this.movie_copy.movie_likability);
          this.dialogEditFormVisible = false;
        }

      },
      addDialogOk(){

      }
    }
  }
</script>

<style scoped>
.button-group {
    margin-top: 20px;
    margin-left: 5px;
}
</style>