<template>
<div class="auther_table_wrap"> 
  <el-table
      :data="specs"
      border
      style="width:95.2%;margin:0px auto;" size="medium" >
      <el-table-column
        prop="id"
        label="id"
        width="100">
      </el-table-column>
      <el-table-column
        prop="name"
        label="规格名称">
      </el-table-column>
      <el-table-column
        prop="spu"
        label="SPU商品名称">
      </el-table-column>
      <el-table-column
        prop="spu_id"
        label="SPU商品id">
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
        <el-form :model="specsForm" status-icon :rules="rulesSpecsForm" ref="specsForm" label-width="100px">
          <el-form-item label="规格名称：" prop="name">
            <el-input type="text" v-model="specsForm.name" autocomplete="off" size="small"></el-input>
          </el-form-item>          
          <el-form-item label="规格：" prop="spu_id">
            <el-select v-model="specsForm.spu_id" size="small">
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
  name: 'AuthorityTable',
  props:['specs'],
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
      goods_list:[],
      specsForm:{
        name:'',
        spu_id:''
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
      this.axios.get(cons.apis + '/goods/specs/'+this.edit_id+'/', {
            headers: {
              'Authorization': 'JWT ' + token
            },
            responseType: 'json',
        })
        .then(dat=>{
            this.specsForm.name = dat.data.name;
            this.specsForm.spu_id = dat.data.spu_id;
        }).catch(err=>{
           console.log(err.response);
      });
  	},
  	submitForm(){
  		this.axios.put(cons.apis + '/goods/specs/'+this.edit_id+'/', {
              "name": this.specsForm.name,
        	    "spu_id": this.specsForm.spu_id,
            }, {
            headers: {
              'Authorization': 'JWT ' + token
            },
            responseType: 'json'           
        }).then(dat=>{
          this.$message({
            type: 'success',
            message: '修改规格成功!'
          }); 
        	this.pop_show = false;
          this.$emit('fnResetTable');           
          this.resetForm('specsForm');          
        }).catch(err=>{
        	console.log(err.response);
        })
  	},
  	fnDelSpecs(id){
        this.edit_id = id;
        this.$confirm('此操作将删除该规格, 是否继续?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          this.axios.delete(cons.apis + '/goods/specs/'+this.edit_id+'/',{
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
                  message:'规格未找到！'
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

<style scope>
.el-table th,.el-table td{
  text-align:center;
}
</style>
