<template>
	<div class="add_user_wrap">
    <el-button type="primary" size="small" @click="pop_show = true" class="pull-right">新增规格</el-button>
    <el-dialog title="新增规格" :visible.sync="pop_show" append-to-body>
        <el-form :model="specsForm" status-icon :rules="rulesSpecsForm" ref="specsForm" label-width="100px">
          <el-form-item label="规格名称：" prop="name">
            <el-input type="text" v-model="specsForm.name" autocomplete="off" size="small"></el-input>
          </el-form-item>
          <el-form-item label="SPU：" prop="spu_id">
            <el-select v-model="specsForm.goods_id" size="small">
              <el-option
                v-for="item in goods_list"
                :key="item.id"
                :label="item.name"
                :value="item.id">
              </el-option>
            </el-select>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="submitForm">提交</el-button>
            <el-button @click="resetForm('specsForm')">重置</el-button>
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
          callback(new Error('规格名不能为空'));
        } else {
          callback()
        }
    };
    return {
      pop_show:false,
      goods_list:[],
      specsForm:{
        name:'',
        goods_id:''
      },
      rulesSpecsForm:{
        name: [
            { validator:validateName, trigger: 'blur' }
        ]
      }
    }
  },
  methods:{
    submitForm(){
        this.axios.post(cons.apis + '/goods/specs/', {
              "name":this.specsForm.name,
              "spu_id":this.specsForm.goods_id
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
                message: '添加规格成功!'
              });
              this.pop_show = false;
              this.$emit('fnResetTable');
              this.resetForm('spcesForm');
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
    fnGetGoods(){
      this.axios.get(cons.apis + '/goods/simple/', {
        headers: {
          'Authorization': 'JWT ' + token
        },
        responseType: 'json',
      })
      .then(dat=>{
          this.goods_list = dat.data;
      }).catch(err=>{
         console.log(err.response);
      });
    },
    resetForm(formName){
      this.$refs[formName].resetFields();
    }
  },
  mounted(){
    this.fnGetGoods();
  }
}
</script>
