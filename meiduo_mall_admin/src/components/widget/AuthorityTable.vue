<template>
<div class="auther_table_wrap"> 
  <el-table
      :data="authors"
      border
      style="width:95.2%;margin:0px auto;" size="medium" >
      <el-table-column
        prop="id"
        label="id"
        width="100">
      </el-table-column>
      <el-table-column
        prop="name"
        label="权限名称">
      </el-table-column>
      <el-table-column
        prop="codename"
        label="权限识别名">
      </el-table-column>
      <el-table-column
      label="操作">
        <template slot-scope="scope">
          <el-button
            size="mini"
            @click="fnPopShow(scope.row.id,scope.row.name,scope.row.codename)">编辑</el-button>
          <el-button
            size="mini"
            type="danger"
            @click="fnDelAuthor(scope.row.id)">删除</el-button>
        </template>
      </el-table-column>
   </el-table>

   <el-dialog title="编辑权限" :visible.sync="pop_show" append-to-body>
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
            <el-button type="primary" @click="submitForm">提交</el-button>
            <el-button @click="pop_show=false">取消</el-button>
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
  props:['authors'],
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
      edit_id:0,
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
  	fnPopShow(id,name,codename){
  		this.pop_show = true;
  		this.edit_id = id;
  		this.authorForm.name = name;
      this.authorForm.codename = codename;
  		
      this.axios.get(cons.apis + '/permission/perms/'+this.edit_id+'/', {
            headers: {
              'Authorization': 'JWT ' + token
            },
            responseType: 'json',
        })
        .then(dat=>{
            this.authorForm.content_type = dat.data.content_type;
        }).catch(err=>{
           console.log(err.response);
      });
  	},
  	fnPopHide(){
  		this.pop_show = false;
	    that.author_ename = '';
	    that.author_type = 0;
  	},
  	submitForm(){
  		this.axios.put(cons.apis + '/permission/perms/'+this.edit_id+'/', {
              "name": this.authorForm.name,
        	    "codename": this.authorForm.codename,
              "content_type": this.authorForm.content_type
            }, {
            headers: {
              'Authorization': 'JWT ' + token
            },
            responseType: 'json'           
        }).then(dat=>{
          this.$message({
            type: 'success',
            message: '修改权限成功!'
          }); 
        	this.pop_show = false;           
          this.resetForm('authorForm');
          this.$emit('fnResetTable');
        }).catch(err=>{
        	console.log(err.response);
        })
  	},
  	fnDelAuthor(id){
        this.edit_id = id;
        this.$confirm('此操作将删除该权限, 是否继续?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          this.axios.delete(cons.apis + '/permission/perms/'+this.edit_id+'/',{
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
    fnGetTypeList(){
      this.axios.get(cons.apis + '/permission/content_types/', {
        headers: {
          'Authorization': 'JWT ' + token
        },
        responseType: 'json',
      })
      .then(dat=>{
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

<style scope>
.el-table th,.el-table td{
  text-align:center;
}
</style>
