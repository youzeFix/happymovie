<template>
<div class="nav-menu-hor">
  <div class="el-menu">
    <el-menu
    :default-active="this.$router.path"
    class="el-menu-demo"
    mode="horizontal"
    background-color="#545c64"
    text-color="#fff"
    active-text-color="#ffd04b"
    router>
    <el-menu-item index="/">电影库</el-menu-item>
    <el-menu-item index="/pick">选电影</el-menu-item>
    <el-submenu index="2">
        <template slot="title">我的工作台</template>
        <el-menu-item index="2-1">选项1</el-menu-item>
        <el-menu-item index="2-2">选项2</el-menu-item>
        <el-menu-item index="2-3">选项3</el-menu-item>
        <el-submenu index="2-4">
        <template slot="title">选项4</template>
        <el-menu-item index="2-4-1">选项1</el-menu-item>
        <el-menu-item index="2-4-2">选项2</el-menu-item>
        <el-menu-item index="2-4-3">选项3</el-menu-item>
        </el-submenu>
    </el-submenu>
    <el-menu-item index="/about">关于</el-menu-item>

    
    <div class="dropdown" v-if="loggedin">
    <el-dropdown @command="handleCommandLogged">
      <span class="el-dropdown-link">
        {{userinfo.nickname}}<i class="el-icon-arrow-down el-icon--right"></i>
      </span>
      <el-dropdown-menu slot="dropdown">
        <el-dropdown-item command="userinfo">个人信息</el-dropdown-item>
        <el-dropdown-item command="logout">退出登录</el-dropdown-item>
      </el-dropdown-menu>
    </el-dropdown>
    </div>

    <div class="dropdown" v-else>
      <el-dropdown @command="handleCommandNotLogged">
      <span class="el-dropdown-link">
        未登录<i class="el-icon-arrow-down el-icon--right"></i>
      </span>
      <el-dropdown-menu slot="dropdown">
        <el-dropdown-item command="login">登录</el-dropdown-item>
        <el-dropdown-item command="register">注册</el-dropdown-item>
      </el-dropdown-menu>
      </el-dropdown>
    </div>
    </el-menu>
  </div>

  <el-dialog title="登录" :visible.sync="dialogLoginVisible">
  <el-form :model="loginForm" v-loading="loginDialogLoading">
    <el-form-item label="用户名">
      <el-input v-model="loginForm.username" ></el-input>
    </el-form-item>
    <el-form-item label="密码">
      <el-input v-model="loginForm.password" show-password></el-input>
    </el-form-item>
    <el-checkbox v-model="keep_login">保持登录</el-checkbox>
  </el-form>
  <div slot="footer" class="dialog-footer">
    <el-button @click="dialogLoginVisible = false">取 消</el-button>
    <el-button type="primary" @click="loginDialogButtonOK()">确 定</el-button>
  </div>
  </el-dialog>

  <el-dialog title="注册" :visible.sync="dialogRegisterVisible">
  <el-form :model="registerForm" v-loading="registerDialogLoading">
    <el-form-item label="昵称">
      <el-input v-model="registerForm.nickname" ></el-input>
    </el-form-item>
    <el-form-item label="用户名">
      <el-input v-model="registerForm.username" ></el-input>
    </el-form-item>
    <el-form-item label="密码">
      <el-input v-model="registerForm.password" show-password></el-input>
    </el-form-item>
  </el-form>
  <div slot="footer" class="dialog-footer">
    <el-button @click="dialogRegisterVisible = false">取 消</el-button>
    <el-button type="primary" @click="registerDialogButtonOK()">确 定</el-button>
  </div>
  </el-dialog>
  
</div>
</template>



<script>
  export default {
    data(){
      return {
        userinfo: {
          userid:0,
          nickname:'',
          username:'',
          usertype:1
        },
        loginForm: {
          username:'',
          password:''
        },
        registerForm: {
          nickname:'',
          username:'',
          password:''
        },
        dialogLoginVisible: false,
        dialogRegisterVisible: false,
        keep_login: false,
        loginDialogLoading: false,
        registerDialogLoading: false
      }
    },
    created: function(){
      console.log('get storage user info')
      let userinfo = localStorage.getItem('userinfo')
      if(userinfo != null){
        userinfo = JSON.parse(userinfo)
        let current_time = (new Date()).valueOf();
        if(current_time - userinfo.time > 7*24*60*60*1000){
          console.log('userinfo expired')
          localStorage.removeItem('userinfo')
          this.$message({
            showClose: true,
            message: '用户信息已过期，请重新登录',
            type: 'error'
          });
        }else{
          this.login(userinfo.username, userinfo.password)
          this.$message({
            showClose: true,
            message: '自动登录',
            type: 'success'
          });
        }
      }
    },
    computed: {
      loggedin(){
        return this.$store.state.logged
      }
    },
    methods: {
      handleCommandLogged(command){
        let that = this;
        switch (command) {
          case "userinfo":
            
            break;

          case "logout":
            console.log('logout');
            this.$axios.get('/auth/logout')
            .then(function(response){
              console.log(response.data);
              if(response.data['statusCode'] == 0){
                that.$message({
                  showClose: true,
                  message: '登出成功',
                  type: 'success'
                });
                that.$store.commit('logged_out')
                localStorage.removeItem('userinfo')
              }else{
                that.$message({
                  showClose: true,
                  message: '登出失败',
                  type: 'error'
                });
              }
            })
            .catch(function(error){
              console.log(error);
            })
            break;
        
          default:
            break;
        }
      },
      handleCommandNotLogged(command){
        switch (command) {
          case "login":
            
            this.dialogLoginVisible = true;
            break;

          case "register":
            this.dialogRegisterVisible = true;
            break;
        
          default:
            break;
        }
      },
      login(username, password){
        let that=this;
        this.loginDialogLoading = true;
        this.$axios({url: '/auth/login',
        method: 'post',
        data: {username: username, password: password},
        transformRequest: [function (data) {
          // Do whatever you want to transform the data
          let ret = ''
          for (let it in data) {
            ret += encodeURIComponent(it) + '=' + encodeURIComponent(data[it]) + '&'
              }
              return ret
        }],
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded'
        }
        })
        .then(function(response){
          console.log(response.data)
          if(response.data['statusCode'] == 0){
            let resp_data = response.data['data']
            that.userinfo.userid = resp_data['id']
            that.userinfo.nickname = resp_data['nickname']
            that.userinfo.username = resp_data['username']
            that.userinfo.usertype = resp_data['usertype']
            that.$store.commit('logged_in')
            that.$message({
              showClose: true,
              message: '登录成功。欢迎回来，'+that.userinfo.nickname+'!',
              type: 'success'
            });
            if(that.keep_login){
              if(localStorage.getItem('userinfo') == null){
                console.log('save user info')
                let timestamp = (new Date()).valueOf();
                localStorage.setItem('userinfo', JSON.stringify({username:username, password:password, time:timestamp}))
              }
            }
          }else if(response.data['statusCode'] == -1){
            that.$message({
              showClose: true,
              message: '登录错误'+response.data['message'],
              type: 'error'
            });
          }
          
        })
        .catch(function(error){
          console.log(error)
        })
        .then(function(){
          that.loginDialogLoading = false;
          that.dialogLoginVisible = false;
        })
      },
      loginDialogButtonOK(){
        this.login(this.loginForm.username, this.loginForm.password)
      },
      registerDialogButtonOK(){
        let that=this;
        this.registerDialogLoading = true;
        this.$axios({url: '/auth/register',
        method: 'post',
        data: {username: this.registerForm.username, password: this.registerForm.password, nickname: this.registerForm.nickname},
        transformRequest: [function (data) {
          // Do whatever you want to transform the data
          let ret = ''
          for (let it in data) {
            ret += encodeURIComponent(it) + '=' + encodeURIComponent(data[it]) + '&'
              }
              return ret
        }],
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded'
        }
        })
        .then(function(response){
          console.log(response.data);
          let statusCode = response.data['statusCode'];
          if(statusCode == 0){
            that.$message({
              showClose: true,
              message: '注册成功',
              type: 'success'
            });
          }else if(statusCode == -1){
            that.$message({
              showClose: true,
              message: '注册失败'+response.data['message'],
              type: 'error'
            });
          }
        })
        .catch(function(error){
          console.log(error)
        })
        .then(function(){
          that.registerDialogLoading = false;
          that.dialogRegisterVisible = false;
        })
      }
    }
    
  }
</script>

<style scoped>
/* .el-menu {
  float: left;
} */
.dropdown {
  float: right;
  margin-top: 20px;
  margin-right: 20px;
  text-align: center;
}
.el-dropdown-link {
  cursor: pointer;
  color: #ffffff;
}
.el-icon-arrow-down {
  font-size: 12px;
}
</style>