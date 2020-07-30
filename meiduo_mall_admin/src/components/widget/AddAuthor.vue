<template>
	<div class="add_user_wrap">
    <el-button type="primary" size="small" @click="pop_show = true" class="pull-right">增加权限</el-button>    
    <el-dialog title="增加权限" :visible.sync="pop_show" append-to-body>
        <el-form :model="authorForm" status-icon :rules="rulesAuthorForm" ref="authorForm" label-width="100px">
          <el-form-item label="权限名称：" prop="name">
            <el-input type="text" v-model="authorForm.name" autocomplete="off" size="small" class="input_width"></el-input>
          </el-form-item>          
          <el-form-item label="权限识别名：" prop="codename">
            <el-input type="text" v-model="authorForm.codename" autocomplete="off" size="small" class="input_width"></el-input>
          </el-form-item>
          <el-form-item label="权限类型：" prop="content_type">
            <el-select v-model="authorForm.content_type" size="small">
              <el-option
                v-for="item in content_type_list"
                :key="item.id"
                :label="item.name"
                :value="item.id">
              </el-option>
            </el-select>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="submitForm()">提交</el-button>
            <el-button @click="resetForm('authorForm')">重置</el-button>
          </el-form-item>
        </el-form>
    </el-dialog>
	</div>  
</template>

<script>
import cons from '@/components/constant';
let token = localStorage.token;
export default {
  name: 'AddUser',
  data () {
    var validateName = (rule, value, callback) => {
        if (value === '') {
          callback(new Error('权限名不能为空'));
        } else {         
          callback()          
        }
    }; 
    var validateType = (rule, value, callback) => {
        if (value === '') {
          callback(new Error('识别名不能为空!'));
        } else {          
          callback()
        }
    }; 
    return {
      pop_show:false,
      content_type_list:[],
      authorForm:{
        name:'',
        codename:'',
        content_type:1
      },
      rulesAuthorForm:{
        name: [
            { validator:validateName, trigger: 'blur' }
        ],
        codename: [
            { validator:validateType, trigger: 'blur' }
        ]
      }
    }
  },
  methods:{
    submitForm(){
        this.axios.post(cons.apis + '/permission/perms/', {
              "name":this.authorForm.name,
              "codename":this.authorForm.codename,
              "content_type":this.authorForm.content_type
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
                message: '添加权限成功!'
              }); 
              this.pop_show = false;           
              this.resetForm('authorForm');
              this.$emit('fnResetTable');                        
            }
        }).catch(err=>{
            if(err.response.status==400){
              var errmsg = err.response.data;

              if(errmsg.name){
                this.$message({
                  type:'info',
                  message:errmsg.name[0]
                });
              }

              if(errmsg.non_field_errors){
                this.$message({
                  type:'info',
                  message:errmsg.non_field_errors[0]
                });
              }           
           }
        });
    },
    fnGetTypeList(){
      this.axios.get(cons.apis + '/permission/content_types/', {
        headers: {
          'Authorization': 'JWT ' + token
        },
        responseType: 'json',
      })
      .then(dat=>{
          //console.log(dat);
          this.content_type_list = dat.data;
      }).catch(err=>{      
         console.log(err.response);
      });
    },
    resetForm(formName){
      this.$refs[formName].resetFields();
    }
  },
  mounted(){
    this.fnGetTypeList();
  }
}
</script>
