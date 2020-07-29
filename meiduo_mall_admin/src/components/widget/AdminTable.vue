<template>
<div class="group_table_wrap">
  <el-table
      :data="admins"
      border
      style="width:95.2%;margin:0px auto;" size="medium" >
      <el-table-column
        prop="id"
        label="id"
        min-width="10">
      </el-table-column>
      <el-table-column
        prop="username"
        label="用户名"
        min-width="25">
      </el-table-column>
      <el-table-column
        prop="email"
        label="邮箱"
        min-width="25">
      </el-table-column>
      <el-table-column
        prop="mobile"
        label="手机号"
        min-width="25">
      </el-table-column>
      <el-table-column
      label="操作"
      min-width="25">
        <template slot-scope="scope">
          <el-button
            size="mini"
            @click="fnPopShow(scope.row.id)">修改</el-button>
          <el-button
            size="mini"
            type="danger"
            @click="fnDelAdmin(scope.row.id)">删除</el-button>
        </template>
      </el-table-column>
   </el-table>
   
   <el-dialog title="管理员信息修改" :visible.sync="pop_show" append-to-body width="95%">
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
  name: 'AdminTable',
  props:['admins'],
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
      edit_id:0,
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
    fnPopShow(id){
      this.pop_show = true;
      this.axios.get(cons.apis + '/permission/admins/'+ id + '/', {
        headers: {
          'Authorization': 'JWT ' + token
        },
        responseType: 'json',
      })
      .then(dat=>{
         this.edit_id = id;
         this.adminForm.username = dat.data.username;
         this.adminForm.password = dat.data.password;
         this.adminForm.mobile = dat.data.mobile;
         this.adminForm.email = dat.data.email;
         this.adminForm.listval = dat.data.groups;
         this.adminForm.listval2 = dat.data.user_permissions;
      }).catch(err=>{      
         console.log(err.response);
      });      
    },
    fnDelAdmin(id){
        this.edit_id = id;
        this.$confirm('此操作将删除该管理员, 是否继续?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          this.axios.delete(cons.apis + '/permission/admins/'+this.edit_id+'/',{
              headers: {
                'Authorization': 'JWT ' + token
              },
              responseType:'json'           
          }).then(dat=>{
            this.$message({
              type: 'success',
              message: '删除成功!'
            });
            this.$emit('fnResetTable');
          }).catch(err=>{
            if(err.response.status==404){
               this.$message({
                  type:'info',
                  message:'管理员未找到！'
                });
            }
          })
        }).catch(() => {
          this.$message({
            type: 'info',
            message: '已取消删除'
          });          
        });     
    },
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
       this.axios.put(cons.apis + '/permission/admins/'+this.edit_id+'/', {
              "username":this.adminForm.username,
              "password":this.adminForm.password,
              "mobile":this.adminForm.mobile,
              "email":this.adminForm.email,
              "groups":this.adminForm.listval,
              "user_permissions":this.adminForm.listval2
            }, {
            headers: {
              'Authorization': 'JWT ' + token
            },
            responseType: 'json'           
        }).then(dat=>{
          this.$message({
            type: 'success',
            message: '管理员信息修改成功!'
          }); 
          this.pop_show = false;                    
          this.resetForm('adminForm');
          this.$emit('fnResetTable');
        }).catch(err=>{
          console.log(err.response);
        })
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

<style scoped>
.el-table th,.el-table td{
  text-align:center;
}
</style>
