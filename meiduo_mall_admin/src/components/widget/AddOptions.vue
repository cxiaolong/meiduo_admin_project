<template>
	<div class="add_options_wrap">
    <el-button type="primary" size="small" @click="pop_show = true" class="pull-right">新增规格选项</el-button>    
    <el-dialog title="新增规格选项" :visible.sync="pop_show" append-to-body>
        <el-form :model="optionsForm" status-icon :rules="rulesoptionsForm" ref="optionsForm" label-width="100px">
          <el-form-item label="选项名称：" prop="name">
            <el-input type="text" v-model="optionsForm.name" autocomplete="off" size="small"></el-input>
          </el-form-item>          
          <el-form-item label="规格：" prop="goods_id">
            <el-select v-model="optionsForm.specs_id" size="small">
              <el-option
                v-for="item in specs_list"
                :key="item.id"
                :label="item.name"
                :value="item.id">
              </el-option>
            </el-select>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="submitForm">提交</el-button>
            <el-button @click="resetForm('optionsForm')">重置</el-button>
          </el-form-item>
        </el-form>
    </el-dialog>
	</div>  
</template>

<script>
import cons from '@/components/constant';
let token = localStorage.token;
export default {
  name: 'AddOption',
  data () {
    var validateName = (rule, value, callback) => {
        if (value === '') {
          callback(new Error('选项名不能为空'));
        } else {         
          callback()          
        }
    }; 
    return {
      pop_show:false,
      specs_list:[],
      optionsForm:{
        name:'',
        specs_id:''
      },
      rulesoptionsForm:{
        name: [
            { validator:validateName, trigger: 'blur' }
        ]
      }
    }
  },
  methods:{
    submitForm(){
        this.axios.post(cons.apis + '/specs/options/', {
              "value":this.optionsForm.name,
              "spec_id":this.optionsForm.specs_id
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
                message: '添加选项成功!'
              }); 
              this.pop_show = false;           
              this.resetForm('optionsForm');
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
    fnGetSpecs(){
      this.axios.get(cons.apis + '/goods/specs/simple/', {
        headers: {
          'Authorization': 'JWT ' + token
        },
        responseType: 'json',
      })
      .then(dat=>{
          this.specs_list = dat.data;        
      }).catch(err=>{      
         console.log(err.response);
      });
    },
    resetForm(formName){
      this.$refs[formName].resetFields();
    }
  },
  mounted(){
    this.fnGetSpecs();
  }
}
</script>
