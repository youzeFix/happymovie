<template>
    <div class="movie-library">
    <div class="button-group">
        <el-button type="success" icon="el-icon-refresh" @click="loadMovieData()">刷新</el-button>
        <el-button-group class="button-group-sub">
        <el-button type="primary" icon="el-icon-edit-outline" @click="editMovieData()" :disabled='edit_disabled'>编辑</el-button>
        <el-button type="primary" icon="el-icon-plus" @click="addMovieData()">新增</el-button>
        <el-button type="danger" icon="el-icon-delete" @click="deleteMovieData()">删除</el-button>
        </el-button-group>
        <el-button-group class="button-group-sub">
        <el-button type="success" icon="el-icon-upload2" @click="bulkImport()">批量导入</el-button>
        <el-button type="primary" icon="el-icon-download" @click="exportMovies()">导出</el-button>
        </el-button-group>

        <el-autocomplete
          class="inline-input search-input"
          prefix-icon="el-icon-search"
          v-model="search_input"
          value-key="name"
          :fetch-suggestions="querySearch"
          placeholder="请输入电影名称"
          :trigger-on-focus="false"
          @select="handleSearchInputSelect"
          clearable
        ></el-autocomplete>
    </div>
    
    <el-table
        ref="singleTable"
        :data="currentPageTableData"
        highlight-current-row
        @current-change="handleCurrentChange"
        style="width: 100%"
        v-loading="loading">
        
        <el-table-column
        type="index"
        width="50"
        :index="tableIndexMethod">
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

    <div class="el-pagination">
      <el-pagination
        background
        :hide-on-single-page="true"
        layout="prev, pager, next"
        :current-page.sync="currentPage"
        :page-size="pageSize"
        :total="tableData.length"
        @current-change="handleCurrentPageChange">
      </el-pagination>
    </div>

    <!-- Form -->
    <el-dialog title="编辑电影" :visible.sync="dialogEditFormVisible">
    <el-form :model="movie_form" v-loading="dialogEditLoading">

        <el-form-item label="电影名称">
        <el-input v-model="movie_form.name" autocomplete="off" disabled></el-input>
        </el-form-item>

        <el-form-item label="主演">
          <el-select
            v-model="movie_form.starring"
            multiple
            filterable
            remote
            allow-create
            :multiple-limit="5"
            placeholder="请输入主演演员"
            :remote-method="remoteStarringMethod"
            :loading="remoteStarringLoading">
            <el-option
              v-for="item in remote_starring"
              :key="item.id"
              :label="item.name"
              :value="item.name">
            </el-option>
          </el-select>
        </el-form-item>

        <el-form-item label="类型">
          <el-select
            v-model="movie_form.genre"
            multiple
            filterable
            remote
            allow-create
            :multiple-limit="6"
            placeholder="请输入电影类型"
            :remote-method="remoteGenreMethod"
            :loading="remoteGenreLoading">
            <el-option
              v-for="item in remote_genre"
              :key="item.id"
              :label="item.genre"
              :value="item.genre">
            </el-option>
          </el-select>
        </el-form-item>

        <el-form-item label="电影时长">
        <el-input-number v-model="movie_form.runtime" controls-position="right" :min="1" :max="1000" disabled></el-input-number>
        分钟
        </el-form-item>

        <el-form-item label="电影评分">
        <el-input-number v-model="movie_form.rating" controls-position="right" :precision="1" :step="0.1" :min="0" :max="10" disabled></el-input-number>
        </el-form-item>

        <el-form-item label="喜爱程度">
        <el-input-number v-model="movie_form.likability" controls-position="right" :min="0" :max="10"></el-input-number>
        </el-form-item>

        <el-form-item label="是否看过">
        <el-switch v-model="movie_form.have_seen"></el-switch>
        </el-form-item>

        <el-form-item label="创建时间">
        <el-date-picker
        v-model="movie_form.create_time"
        type="datetime"
        placeholder="选择日期时间"
        disabled>
        </el-date-picker>
        </el-form-item>

        <el-form-item label="备注">
        <el-input type="textarea" v-model="movie_form.comment"></el-input>
        </el-form-item>
    </el-form>
    <div slot="footer" class="dialog-footer">
        <el-button @click="dialogEditFormVisible = false">取 消</el-button>
        <el-button type="primary" @click="editDialogOk()">确 定</el-button>
    </div>
    </el-dialog>


    <el-dialog title="新增电影" :visible.sync="dialogAddFormVisible">
    <el-form :model="movie_form" :rules="add_dialog_rules" v-loading="dialogAddLoading" ref="movie_form">
        <el-form-item label="电影名称" prop='name'>
        <el-input v-model="movie_form.name" autocomplete="off"></el-input>
        </el-form-item>

        <el-form-item label="主演">
          <el-select
            v-model="movie_form.starring"
            multiple
            filterable
            remote
            allow-create
            :multiple-limit="5"
            placeholder="请输入主演演员"
            :remote-method="remoteStarringMethod"
            :loading="remoteStarringLoading">
            <el-option
              v-for="item in remote_starring"
              :key="item.id"
              :label="item.name"
              :value="item.name">
            </el-option>
          </el-select>
        </el-form-item>

        <el-form-item label="类型">
          <el-select
            v-model="movie_form.genre"
            multiple
            filterable
            remote
            allow-create
            :multiple-limit="6"
            placeholder="请输入电影类型"
            :remote-method="remoteGenreMethod"
            :loading="remoteGenreLoading">
            <el-option
              v-for="item in remote_genre"
              :key="item.id"
              :label="item.genre"
              :value="item.genre">
            </el-option>
          </el-select>
        </el-form-item>

        <el-form-item label="电影时长">
        <el-input-number v-model="movie_form.runtime" controls-position="right" :min="1" :max="1000"></el-input-number>
        分钟
        </el-form-item>

        <el-form-item label="电影评分">
        <el-input-number v-model="movie_form.rating" controls-position="right" :precision="1" :step="0.1" :min="0" :max="10"></el-input-number>
        </el-form-item>

        <el-form-item label="喜爱程度">
        <el-input-number v-model="movie_form.likability" controls-position="right" :min="0" :max="10"></el-input-number>
        </el-form-item>

        <el-form-item label="是否看过">
        <el-switch v-model="movie_form.have_seen"></el-switch>
        </el-form-item>

        <el-form-item label="创建时间">
        <el-date-picker
        v-model="movie_form.create_time"
        type="datetime"
        placeholder="选择日期时间"
        value-format='yyyy-MM-dd HH:mm:ss'>
        </el-date-picker>
        </el-form-item>

        <el-form-item label="备注">
        <el-input type="textarea" v-model="movie_form.comment"></el-input>
        </el-form-item>
    </el-form>
    <div slot="footer" class="dialog-footer">
        <el-button @click="dialogAddFormVisible = false">取 消</el-button>
        <el-button type="primary" @click="addDialogOk()">确 定</el-button>
    </div>
    </el-dialog>

    <!-- 批量导入对话框 -->
    <el-dialog class="dialog-batch-import" title="批量导入" :visible.sync="bulkImportDialogVisible">
      <el-upload
        class="upload-demo"
        ref="upload"
        drag
        action="/files/upload"
        multiple
        :auto-upload="false"
        :file-list="fileList"
        :on-success="fileUploadSuccess"
        :on-error="fileUploadError"
        accept=".xlsx">
        <i class="el-icon-upload"></i>
        <div class="el-upload__text">将文件拖到此处，或<em>点击选择</em></div>
        <div class="el-upload__tip" slot="tip">只能上传jpg/png文件，且不超过500kb</div>
      </el-upload>
      <div slot="footer" class="dialog-footer">
        <el-button type="success" @click="download_movies_template()">下载模板</el-button>
        <el-button type="primary" @click="bulkImportDialogOK()">上传</el-button>
        <el-button @click="bulkImportDialogVisible = false">取 消</el-button>
      </div>
    </el-dialog>
    
    </div>
</template>

<script>
  export default {
    name: 'movie-library',
    data() {
      return {
        tableData: [],
        currentPageTableData: [],
        currentRow: null,
        loading: false,
        edit_disabled: true,
        dialogEditFormVisible: false,
        dialogAddFormVisible: false,
        movie_form: {
            id: 0,
            name: '',
            starring:[],
            genre:[],
            runtime: '',
            rating: '',
            likability: '',
            have_seen: '',
            create_time: '',
            comment: ''
        },
        dialogEditLoading: false,
        dialogAddLoading: false,
        add_dialog_rules: {
          name: [
            {required: true, message:'请输入电影名称', trigger: 'blur'}
          ]
        },
        bulkImportDialogVisible: false,
        fileList: [],
        currentPage: 1,
        pageSize: 11,
        search_input: '',
        remote_starring: [],
        remote_genre: [],
        remoteStarringLoading: false,
        remoteGenreLoading: false
      }
    },
    computed: {
      loggedin(){
        return this.$store.state.logged
      }
    },
    watch: {
      loggedin: function(newState){
        // console.log('new' + newState)
        if(newState){
          this.loadMovieData()
        }else{
          this.tableData = []
          this.currentPageTableData = []
        }
      }
    },

    methods: {
      remoteStarringMethod(query){
        if (query !== '') {
          this.remoteStarringLoading = true;
          let that = this;
          this.$axios.get('/movie/starrings', {params: {filter: query}})
          .then(function(response){
            let data = response.data
            if(data['statusCode'] == 0){
              that.remote_starring = data['data']
            }else{
              that.remote_starring = []
            }
          })
          .catch(function(error){
            console.log(error)
          })
          .then(function(){
            that.remoteStarringLoading = false
          })
          
        } else {
          this.remote_starring = [];
        }
      },
      remoteGenreMethod(query){
        if (query !== '') {
          this.remoteGenreLoading = true;
          let that = this
          this.$axios.get('/movie/genres', {params: {filter: query}})
          .then(function(response){
            console.log(response)
            let data = response.data
            if(data['statusCode'] == 0){
              that.remote_genre = data['data']
            }else{
              that.remote_genre = []
            }
          })
          .catch(function(error){
            console.log(error)
          })
          .then(function(){
            that.remoteGenreLoading = false
          })
          
        } else {
          this.remote_genre = [];
        }
      },
      tableListFormatter(row, column, cellValue){
        if(cellValue){
          return cellValue.join("/")
        }
      },
      haveSeenFormatter(row, column, cellValue){
        if(cellValue == true){
          return '是'
        }else if(cellValue == false){
          return '否'
        }
      },
      querySearch(queryString, cb) {
        let results = queryString ? this.tableData.filter(this.createSearchFilter(queryString)) : this.tableData;
        // 调用 callback 返回建议列表的数据
        console.log(queryString)
        console.log(results)
        cb(results);
      },
      createSearchFilter(queryString) {
        return (movie) => {
          // console.log(movie.movie_name)
          return (movie.name.toLowerCase().indexOf(queryString.toLowerCase()) != -1);
        };
      },
      handleSearchInputSelect(item) {
        console.log(item);
        let index = this.tableData.indexOf(item)+1
        let pageNum = Math.ceil(index/this.pageSize)
        console.log('pageNum is'+pageNum)
        this.currentPage = pageNum;
        this.updateCurrentPageTableData();
        this.setCurrent(item);
      },
      tableIndexMethod(index){
        return this.pageSize*(this.currentPage-1)+1+index
      },
      updateCurrentPageTableData(){
        let startIndex = (this.currentPage-1)*this.pageSize
        this.currentPageTableData = this.tableData.slice(startIndex, startIndex+this.pageSize)
      },
      handleCurrentPageChange(){
        // this.currentPage = newPage
        console.log('current page is '+this.currentPage)
        this.updateCurrentPageTableData()
      },
      download_movies_template(){
        let fileUrl = '/files/download/movies-template.xlsx'
        window.open(fileUrl)
        // window.location.href = fileUrl
      },
      setCurrent(row) {
        this.$refs.singleTable.setCurrentRow(row);
        if(!row){
            this.edit_disabled=true;
        }
      },
      bulkImport(){
        this.bulkImportDialogVisible = true
      },
      submitUpload(){
        console.log(this.fileList)
      },
      bulkImportDialogOK(){
        console.log('start upload')
        this.$refs.upload.submit()
      },
      fileUploadSuccess(response){
        console.log('file upload success')
        console.log(response)
        this.$message({
          showClose: true,
          message: '导入成功',
          type: 'success'
        });
        this.loadMovieData()
      },
      fileUploadError(err){
        console.log('file upload error')
        console.log(err)
        this.$message({
          showClose: true,
          message: '导入失败',
          type: 'error'
        });
      },
      handleCurrentChange(val) {
        this.currentRow = val;
        this.edit_disabled=false;
      },
      loadMovieData(){
        if(!this.loggedin){
          this.$message({
              showClose: true,
              message: '请登录后操作',
              type: 'error'
            });
          return
        }
        this.loading=true
        let that = this;
        this.$axios.get('/movie/all')
        .then(function (response){
          console.log(response.data)
          let statusCode = response.data['statusCode']
          if(statusCode == 0){
            that.tableData = response.data['data'];
            that.updateCurrentPageTableData()
          }else if(statusCode == -1){
            that.$message({
              showClose: true,
              message: '请登录后操作',
              type: 'error'
            })
          }
            
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
        if(!this.loggedin){
          this.$message({
              showClose: true,
              message: '请登录后操作',
              type: 'error'
            });
          return
        }
          console.log(this.currentRow);
          if(!this.currentRow){
            this.$message({
              showClose: true,
              message: '请选择一行',
              type: 'error'
            });
          }
          else
          {
            this.movie_form.id = this.currentRow.id;
            this.movie_form.name = this.currentRow.name;
            this.movie_form.starring = this.currentRow.starring;
            this.movie_form.genre = this.currentRow.genre;
            this.movie_form.runtime = this.currentRow.runtime;
            this.movie_form.rating = this.currentRow.rating;
            this.movie_form.likability = this.currentRow.likability;
            this.movie_form.have_seen = this.currentRow.have_seen;
            this.movie_form.create_time = this.currentRow.create_time;
            this.movie_form.comment = this.currentRow.comment;
            this.movie_copy = Object.assign({}, this.movie_form);
            this.dialogEditFormVisible = true;
          }
          
      },
      editDialogOk(){
        let movie_form_changed = false
        let prop_diff = {};
        for(let prop in this.movie_copy){
            if(this.movie_copy[prop] != this.movie_form[prop]){
              prop_diff[prop]=this.movie_form[prop];
              movie_form_changed = true
            }
          }
        if(movie_form_changed){
          console.log('movie_form is changed');
          if(Object.keys(prop_diff).length){
            prop_diff['id'] = this.movie_copy.id;
            const headerJSON = {
                "Content-Type": "application/json"
            };
            let that = this;
            this.dialogEditLoading = true;
            this.$axios.put('/movie/', prop_diff, {headers:headerJSON})
            .then(function(response){
              console.log('update success'+response.data);
              let id = prop_diff['id'];
              delete prop_diff['id'];
              for(let i=0; i< that.tableData.length; i++){
                let ele = that.tableData[i];
                if(ele['id'] == id){
                  // console.log('find it')
                  for(let prop in prop_diff){
                    ele[prop] = prop_diff[prop];
                  }
                  break;
                }
              }
              that.$message({
              showClose: true,
              message: '修改成功',
              type: 'success'
              })
            })
            .catch(function(error){
              console.log(error);
            })
            .then(function(){
              that.dialogEditLoading=false;
              that.dialogEditFormVisible = false;
            })
          }
        }else{
          console.log('movie not change'+this.movie_form.likability+this.movie_copy.likability);
          this.dialogEditFormVisible = false;
        }

      },
      addMovieData(){
        if(!this.loggedin){
          this.$message({
              showClose: true,
              message: '请登录后操作',
              type: 'error'
            });
          return
        }
        Object.keys(this.movie_form).forEach(key => this.movie_form[key] = '');
        this.movie_form.have_seen = 0;
        this.dialogAddFormVisible = true;
      },
      addDialogOk(){
        let isValid = false;
        this.$refs["movie_form"].validate((valid) => {
          if(valid){
            isValid = true
          }else{
            console.log('valid fail')
          }
        })
        if(!isValid)return;
        let that = this;
        this.dialogAddLoading = true;
        this.$axios.post('/movie/', {
          'name': this.movie_form.name,
          'starring': this.movie_form.starring.map(function(item) { return item.trim(); }),
          'genre': this.movie_form.genre.map(function(item) { return item.trim(); }),
          'runtime': this.movie_form.runtime,
          'rating': this.movie_form.rating,
          'likability': this.movie_form.likability,
          'have_seen': this.movie_form.have_seen,
          'create_time': this.movie_form.create_time,
          'comment': this.movie_form.comment
        })
        .then(function(response){
          console.log(response.data);
          if(response.data['statusCode'] == -1){
            that.$message({
              showClose: true,
              message: '请登录后操作',
              type: 'error'
            });
          }else{
            that.tableData.push(response.data['data']);
            that.$message({
              showClose: true,
              message: '新增成功',
              type: 'success'
            })
            that.updateCurrentPageTableData()
          }
          
        })
        .catch(function(error){
          console.log(error)
        })
        .then(function(){
          that.dialogAddLoading = false;
          that.dialogAddFormVisible=false;
        })
      },
      deleteMovieData(){
        if(!this.loggedin){
          this.$message({
              showClose: true,
              message: '请登录后操作',
              type: 'error'
            });
          return
        }
        if(!this.currentRow){
            this.$message({
              showClose: true,
              message: '请选择一行',
              type: 'error'
            });
            return
        }
        let id = this.currentRow.id;
        let that = this;
        let table_index = -1;
        for(let i=0; i<this.tableData.length; i++){
          if(this.tableData[i]['id'] == id){
            table_index = i;
            break;
          }
        }
        console.log(this.currentRow+table_index);

        this.loading = true;
        this.$axios.delete('/movie/',{params:{'id':id}})
        .then(function(response){
          console.log(response.data);
          let statusCode = response.data['statusCode']
          if(statusCode == 0){
            that.tableData.splice(table_index, 1);
            that.$message({
              showClose: true,
              message: '删除成功',
              type: 'success'
            })
            that.updateCurrentPageTableData()
            if(that.currentPageTableData.length > 0){
              that.setCurrent(that.currentPageTableData[0])
            }
          }else if(statusCode == -1){
            that.$message({
              showClose: true,
              message: '请登录后操作',
              type: 'error'
            })
          }
        })
        .catch(function(error){
          console.log(error);
        })
        .then(function(){
          that.loading = false;
        })
      },
      exportMovies(){
        if(!this.loggedin){
          this.$message({
              showClose: true,
              message: '请登录后操作',
              type: 'error'
            });
          return
        }
        let that = this;
        this.loading = true;
        this.$axios.get('/movie/export')
        .then(function(response){
          console.log(response.data);
          let statusCode = response.data['statusCode']
          if(statusCode == 0){
            that.$message({
              showClose: true,
              message: '导出成功',
              type: 'success'
            })
            let fileUrl = '/files/download/' + response.data['data']['filename']
            window.open(fileUrl)
          }else if(statusCode == -1){
            that.$message({
              showClose: true,
              message: '请登录后操作',
              type: 'error'
            })
          }
        })
        .catch(function(error){
          console.log(error);
        })
        .then(function(){
          that.loading = false;
        })
      }
    }
  }
</script>

<style scoped>
.button-group {
    margin-top: 20px;
    margin-left: 8px;
}
.button-group-sub {
  margin-left: 10px;
}
.dialog-footer {
  text-align: center;
  padding-bottom: 10px;
}
.el-pagination {
  text-align: center;
  margin-top: 10px;
  margin-bottom: 10px;
}
.dialog-batch-import {
  text-align: center;
  /* width: 50%; */
}
.search-input {
  margin-left: 10px;
}
</style>