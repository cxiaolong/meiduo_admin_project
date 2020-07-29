<template>
	<div class="add_user_wrap">
    <el-button type="primary" size="small"  @click="pop_show = true">增加用户</el-button>
      <el-dialog title="增加用户" :visible.sync="pop_show" append-to-body>
        <el-form :model="userForm" status-icon :rules="rulesUserForm" ref="userForm" label-width="100px">
          <el-form-item label="用户名:" prop="username">
            <el-input type="text" v-model="userForm.username" autocomplete="off" size="small" class="input_width"></el-input>
          </el-form-item>
          <el-form-item label="密码:" prop="password">
            <el-input type="password" v-model="userForm.password" autocomplete="off" size="small" class="input_width"></el-input>
          </el-form-item>
          <el-form-item label="确认密码:" prop="passcheck">
            <el-input type="password" v-model="userForm.passcheck" autocomplete="off" size="small" class="input_width"></el-input>
          </el-form-item>
          <el-form-item label="手机号:" prop="mobile">
            <el-input type="text" v-model="userForm.mobile" autocomplete="off" size="small" class="input_width"></el-input>
          </el-form-item>
          <el-form-item label="邮箱:" prop="email">
            <el-input type="text" v-model="userForm.email" autocomplete="off" size="small" class="input_width"></el-input>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="submitForm('userForm')">提交</el-button>
            <el-button @click="resetForm('userForm')">重置</el-button>
          </el-form-item>
        </el-form>
      </el-dialog>
	</div>  
</template>

<script>
import cons from '@/components/constant';
export default {
  name: 'AddUser',
  data () {
    var validateUserName = (rule, value, callback) => {
        if (value === '') {
          callback(new Error('用户名不能为空!'));
        } else {
          var reUser = /^\w{5,20}$/;
          if(reUser.test(value))
          {
            callback()
          }else{
             callback(new Error('用户名是5到20位数字、字母或下划线'));
          }
        }
    }; 
    var validatePassWord = (rule, value, callback) => {
        if (value === '') {
          callback(new Error('密码不能为空!'));
        } else {
          var rePass = /^[\w!@#$%^&*]{8,20}$/;
          if(rePass.test(value))
          {
            callback()
          }else{
             callback(new Error('密码是8到20位数字、字母或下划线以及特殊!@#$%^&*符号'));
          }
        }
    }; 
    var validatePassCheck = (rule, value, callback) => {
        if (value === '') {
          callback(new Error('请再次输入密码'));
        } else if (value !== this.userForm.password) {
          callback(new Error('两次输入密码不一致!'));
        } else {
          callback();
        }
    };
    var validateMobile = (rule, value, callback) => {
        if (value === '') {
          callback(new Error('手机号不能为空!'));
        } else {
          var rePhone = /^1[34578]\d{9}$/;
          if(rePhone.test(value))
          {
            callback()
          }else{
             callback(new Error('手机格式不正确'));
          }
        }
    };    
    return {
      pop_show:false,
      userForm:{
        username:'',
        password:'',
        passcheck:'',
        mobile:'',
        email:''
      },
      rulesUserForm:{
        username: [
            { validator: validateUserName, trigger: 'blur' }
        ],
        password: [
            { validator: validatePassWord, trigger: 'blur' }
        ],
        passcheck: [
            { validator: validatePassCheck, trigger: 'blur' }
        ],
        mobile: [
            { validator: validateMobile, trigger: 'blur' }
        ]
      }
    }
  },
  methods:{  
    submitForm(formName){
      this.$refs[formName].validate((valid) => {
        if (valid) {
        let token = localStorage.token;
        this.axios.post(cons.apis + '/users/', {
              "username": this.userForm.username,
              "mobile": this.userForm.mobile,
              "password": this.userForm.password,
              "email": this.userForm.email
            }, {
            headers: {
              'Authorization': 'JWT ' + token
            },
            responseType: 'json'           
        })
        .then(dat=>{
            if(dat.status==201){
              this.$message({
                type: 'success',
                message: '添加用户成功!'
              });
              this.$emit('fnSetKey',this.userForm.username);             
              this.pop_show = false;
              this.resetForm('userForm');                     
            }
        }).catch(err=>{
           if(err.response.status==400){
              var errmsg = err.response.data;
              if(errmsg.username){
                this.$message({
                  type: 'info',
                  message: errmsg.username[0]
                });
              }
              if(errmsg.password){
                this.$message({
                  type: 'info',
                  message:errmsg.password[0]
                });
              }
              if(errmsg.mobile){
                this.$message({
                  type: 'info',
                  message:errmsg.mobile[0]
                });
              }
              if(errmsg.email){
                this.$message({
                  type: 'info',
                  message:errmsg.email[0]
                });
              }
           }
        });
        } else {
          console.log('error submit!!');
          return false;
        }
      });
    },
    resetForm(formName){
      this.$refs[formName].resetFields();
    }
  }
}
</script>

<style scoped>
.input_width{
  width:450px;
}
</style>
