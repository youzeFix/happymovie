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
  <el-form :model="form">
    <el-form-item label="用户名">
      <el-input v-model="loginForm.username" ></el-input>
    </el-form-item>
    <el-form-item label="密码">
      <el-input v-model="loginForm.password" show-password></el-input>
    </el-form-item>
  </el-form>
  <div slot="footer" class="dialog-footer">
    <el-button @click="dialogLoginVisible = false">取 消</el-button>
    <el-button type="primary" @click="dialogLoginVisible = false">确 定</el-button>
  </div>
  </el-dialog>

  <el-dialog title="注册" :visible.sync="dialogRegisterVisible">
  <el-form :model="form">
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
    <el-button type="primary" @click="dialogRegisterVisible = false">确 定</el-button>
  </div>
  </el-dialog>
  
</div>
</template>



<script>
  export default {
    data(){
      return {
        loggedin: false,
        userinfo: {
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
        dialogRegisterVisible: false
      }
    },
    methods: {
      handleCommandLogged(command){
        switch (command) {
          case "userinfo":
            
            break;

          case "logout":
            
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