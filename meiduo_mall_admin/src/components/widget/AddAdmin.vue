<template>
	<div class="add_admin_wrap">
     <el-button type="primary" size="small" @click="pop_show = true" class="pull-right">新增管理员</el-button>     
     <el-dialog title="新增管理员" :visible.sync="pop_show" append-to-body width="95%">
        <el-form :model="adminForm" :inline="true" status-icon :rules="rulesAdminForm" ref="adminForm" label-width="70px">
          <el-form-item label="用户名：" prop="username">
            <el-input type="text" v-model="adminForm.username" autocomplete="off" size="small"></el-input>
          </el-form-item>          
          <el-form-item label="密码：" prop="password">
            <el-input type="text" v-model="adminForm.password" autocomplete="off" size="small"></el-input>
          </el-form-item>
          <el-form-item label="手机：" prop="mobile">
            <el-input type="text" v-model="adminForm.mobile" autocomplete="off" size="small"></el-input>
          </el-form-item>
          <el-form-item label="邮箱：" prop="email">
            <el-input type="text" v-model="adminForm.email" autocomplete="off" size="small"></el-input>
          </el-form-item>
          <el-form-item label="用户组：">
            <el-transfer v-model="adminForm.listval" :data="adminForm.list" size="mini"></el-transfer>
          </el-form-item>
          <el-form-item label="权限：">
            <el-transfer v-model="adminForm.listval2" :data="adminForm.list2" size="mini"></el-transfer>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="submitForm">提交</el-button>
            <el-button @click="resetForm('adminForm')">重置</el-button>
          </el-form-item>
        </el-form>
    </el-dialog>
	</div>  
</template>

<script>
import cons from '@/components/constant';
let token = localStorage.token;
export default {
  name: 'AddAdmin',
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
      adminForm:{
        username:'',
        password:'',
        mobile:'',
        email:'',
        list:[],
        listval:[],
        list2:[],
        listval2:[]
      },
      rulesAdminForm:{
        username: [
            { validator: validateUserName, trigger: 'blur' }
        ],
        password: [
            { validator: validatePassWord, trigger: 'blur' }
        ],
        mobile: [
            { validator: validateMobile, trigger: 'blur' }
        ]
      }
    }
  },
  methods:{
    fnGetPower(){
      this.axios.get(cons.apis + '/permission/simple/', {
          headers: {
            'Authorization': 'JWT ' + token
          },
          responseType: 'json'
      })
      .then(dat=>{
          var aList = dat.data;
          var aList2 = [];
          for(var i=0;i<aList.length;i++){
            aList2.push({key:aList[i].id,label:aList[i].name})
          }
          this.adminForm.list2 = aList2;        
      }).catch(err=>{
         console.log(err);
      });
    },
    fnGetGroup(){
      this.axios.get(cons.apis + '/permission/groups/simple/', {
          headers: {
            'Authorization': 'JWT ' + token
          },
          responseType: 'json'
      })
      .then(dat=>{
          var aList = dat.data;
          var aList2 = [];
          for(var i=0;i<aList.length;i++){
            aList2.push({key:aList[i].id,label:aList[i].name})
          }
          this.adminForm.list = aList2;        
      }).catch(err=>{
         console.log(err);
      });
    },
    submitForm(){
       this.axios.post(cons.apis + '/permission/admins/', {
              "username":this.adminForm.username,
              "password":this.adminForm.password,
              "mobile":this.adminForm.mobile,
              "email":this.adminForm.email,
              "groups":this.adminForm.listval,
              "user_permissions":this.adminForm.listval2,
            },{
            headers: {
              'Authorization': 'JWT ' + token
            },
            responseType: 'json'           
        })
        .then(dat=>{
            if(dat.status==201){
              this.$message({
                type: 'success',
                message: '添加管理员成功!'
              });
              this.pop_show = false;            
              this.adminForm.name = '';
              this.adminForm.listval = [];
              this.adminForm.listval2 = [];
              this.resetForm('adminForm')
              this.$emit('fnResetTable');                        
            }
        }).catch(err=>{
           if(err.response.status==400){
               this.$message({
                  type:'info',
                  message:err.response.data.name[0]
              });
           }          
        }); 
    },
    resetForm(formName){
      this.$refs[formName].resetFields();
    }
  },
  mounted(){
    this.fnGetPower();
    this.fnGetGroup();
  }
}
</script>


