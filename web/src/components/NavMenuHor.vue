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
  <el-form :model="loginForm" status-icon ref="loginForm" :rules="loginRules" v-loading="loginDialogLoading">
    <el-form-item label="用户名" prop="username">
      <el-input v-model="loginForm.username" placeholder="请输入6-16位字母或数字"></el-input>
    </el-form-item>
    <el-form-item label="密码" prop="password">
      <el-input v-model="loginForm.password" show-password placeholder="请输入6-16位字母或数字"></el-input>
    </el-form-item>
    <el-checkbox v-model="keep_login">保持登录</el-checkbox>
  </el-form>
  <div slot="footer" class="dialog-footer">
    <el-button @click="dialogLoginVisible = false">取 消</el-button>
    <el-button type="primary" @click="loginDialogButtonOK()">确 定</el-button>
  </div>
  </el-dialog>

  <el-dialog title="注册" :visible.sync="dialogRegisterVisible">
  <el-form :model="registerForm" status-icon ref="registerForm" :rules="registerRules" v-loading="registerDialogLoading">
    <el-form-item label="昵称" prop="nickname">
      <el-input v-model="registerForm.nickname" maxlength=10></el-input>
    </el-form-item>
    <el-form-item label="用户名" prop="username">
      <el-input v-model="registerForm.username" maxlength=16 placeholder="请输入6-16位字母或数字"></el-input>
    </el-form-item>
    <el-form-item label="密码" prop="password">
      <el-input v-model="registerForm.password" show-password maxlength=16 placeholder="请输入6-16位字母或数字"></el-input>
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
      var validateNickname = (rule, value, callback) => {
        callback();
      };
      var validateUsername = (rule, value, callback) => {
        if (!value) {
          return callback(new Error('用户名不能为空'));
        }
        let p = /^\w\w{5,15}$/;
        let r = p.test(value);//校验
        if(!r){
          callback(new Error('请输入6-16位字母或数字'));
        }else{
          callback();
        }
        // setTimeout(() => {
        //   let p = /^\w\w{5,15}$/;
        //   let r = p.test(value);//校验
        //   if(!r){
        //     callback(new Error('请输入6-16位字母或数字'));
        //   }else{
        //     callback();
        //   }
        // }, 1000);
      };
      var validatePassword = (rule, value, callback) => {
        if (!value) {
          return callback(new Error('密码不能为空'));
        }
        let p = /^\w\w{5,15}$/;
        let r = p.test(value);//校验
        if(!r){
          callback(new Error('请输入6-16位字母或数字'));
        }else{
          callback();
        }
      };
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
        registerDialogLoading: false,
        registerRules: {
          nickname: [
            { validator: validateNickname, trigger: 'blur' }
          ],
          username: [
            { required: true, validator: validateUsername, trigger: 'blur' }
          ],
          password: [
            { required: true, validator: validatePassword, trigger: 'blur' }
          ]
        },
        loginRules: {
          username: [
            { required: true, validator: validateUsername, trigger: 'blur' }
          ],
          password: [
            { required: true, validator: validatePassword, trigger: 'blur' }
          ]
        }
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
        let isValid = false
        this.$refs['loginForm'].validate((valid) => {
          if(valid){
            isValid = true
          }else{
            console.log('valid fail')
          }
        })
        if(!isValid)return;
        this.login(this.loginForm.username, this.loginForm.password)
      },
      registerDialogButtonOK(){
        let isValid = false
        this.$refs['registerForm'].validate((valid) => {
          if(valid){
            isValid = true
          }else{
            console.log('valid fail')
          }
        })
        if(!isValid)return;
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