<template>
<div class="auther_table_wrap"> 
  <el-table
      :data="options"
      border
      style="width:95.2%;margin:0px auto;" size="medium" >
      <el-table-column
        prop="id"
        label="id"
        width="100">
      </el-table-column>
      <el-table-column
        prop="value"
        label="规格选项名称">
      </el-table-column>
      <el-table-column
        prop="spec_id"
        label="规格id">
      </el-table-column>
      <el-table-column
        prop="spec"
        label="规格名称">
      </el-table-column>
      <el-table-column
      label="操作">
        <template slot-scope="scope">
          <el-button
            size="mini"
            @click="fnPopShow(scope.row.id)">编辑</el-button>
          <el-button
            size="mini"
            type="danger"
            @click="fnDelSpecs(scope.row.id)">删除</el-button>
        </template>
      </el-table-column>
   </el-table>

    <el-dialog title="修改规格" :visible.sync="pop_show" append-to-body>
        <el-form :model="optionsForm" status-icon :rules="rulesSpecsForm" ref="optionsForm" label-width="100px">
          <el-form-item label="规格名称：" prop="name">
            <el-input type="text" v-model="optionsForm.name" autocomplete="off" size="small"></el-input>
          </el-form-item>          
          <el-form-item label="规格：" prop="spec_id">
            <el-select v-model="optionsForm.spec_id" size="small">
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
  name: 'OptionsTable',
  props:['options'],
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
      edit_id:'',
      specs_list:[],
      optionsForm:{
        name:'',
        spec_id:''
      },
      rulesSpecsForm:{
        name: [
            { validator:validateName, trigger: 'blur' }
        ]
      }
    }
  },
  methods:{
  	fnPopShow(id){
  		this.pop_show = true;
      this.edit_id = id;
      this.axios.get(cons.apis + '/specs/options/'+this.edit_id+'/', {
            headers: {
              'Authorization': 'JWT ' + token
            },
            responseType: 'json',
        })
        .then(dat=>{
            //console.log(dat);
            this.optionsForm.name = dat.data.value;
            this.optionsForm.spec_id = dat.data.spec_id;
        }).catch(err=>{
           console.log(err.response);
      });
  	},
  	submitForm(){
  		this.axios.put(cons.apis + '/specs/options/'+this.edit_id+'/', {
              "value":this.optionsForm.name,
              "spec_id":this.optionsForm.spec_id
            }, {
            headers: {
              'Authorization': 'JWT ' + token
            },
            responseType: 'json'           
        }).then(dat=>{
          this.$message({
            type: 'success',
            message: '修改规格选项成功!'
          }); 
        	this.pop_show = false;
          this.$emit('fnResetTable');         
          this.resetForm('optionsForm');          
        }).catch(err=>{
        	console.log(err.response);
        })
  	},
  	fnDelSpecs(id){
        this.edit_id = id;
        this.$confirm('此操作将删除该规格选项, 是否继续?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          this.axios.delete(cons.apis + '/specs/options/'+this.edit_id+'/',{
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
                  message:'权限未找到！'
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

<style scope>
.el-table th,.el-table td{
  text-align:center;
}
</style>
