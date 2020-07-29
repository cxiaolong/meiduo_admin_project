<template>
<div class="group_table_wrap">
  <el-table
      :data="groups"
      border
      style="width:95.2%;margin:0px auto;" size="medium" >
      <el-table-column
        prop="id"
        label="id"
        min-width="10">
      </el-table-column>
      <el-table-column
        prop="name"
        label="组名称"
        min-width="60">
      </el-table-column>
      <el-table-column
      label="操作"
      min-width="30">
        <template slot-scope="scope">
          <el-button
            size="mini"
            @click="fnPopShow(scope.row.id)">修改</el-button>
          <el-button
            size="mini"
            type="danger"
            @click="fnDelGroup(scope.row.id)">删除</el-button>
        </template>
      </el-table-column>
   </el-table>

   <el-dialog title="增加用户组" :visible.sync="pop_show" append-to-body width="54%">
        <el-form :model="groupForm" status-icon :rules="rulesGroupForm" ref="groupForm" label-width="100px">
          <el-form-item label="名称：" prop="name">
            <el-input type="text" v-model="groupForm.name" autocomplete="off" size="small" class="input_width"></el-input>
          </el-form-item>
          <el-form-item label="权限：">
             <el-transfer v-model="groupForm.listval" :data="groupForm.list"></el-transfer>
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
  name: 'GroupTable',
  props:['groups'],
  data () {
    var validateName = (rule, value, callback) => {
        if (value === '') {
          callback(new Error('组名不能为空'));
        } else {         
          callback()          
        }
    }; 
    return {
      pop_show:false,
      edit_id:0,
      groupForm:{
        name:'',
        list:[],
        listval:[]
      },
      rulesGroupForm:{
        name: [
            { validator:validateName, trigger: 'blur'}
        ]
      }
    }
  },
  methods:{
  	fnGetPowerList(){
      this.axios.get(cons.apis + '/permission/simple/', {
        headers: {
          'Authorization': 'JWT ' + token
        },
        responseType: 'json',
      })
      .then(dat=>{
          var aList = dat.data;
          var aList2 = [];
          for(var i=0;i<aList.length;i++){
            aList2.push({key:aList[i].id,label:aList[i].name})
          }
          this.groupForm.list = aList2;       
      }).catch(err=>{      
         console.log(err.response);
      });
    },
    fnPopShow(id){
       this.pop_show = true;
       this.axios.get(cons.apis + '/permission/groups/'+ id + '/', {
        headers: {
          'Authorization': 'JWT ' + token
        },
        responseType: 'json',
      })
      .then(dat=>{
         this.edit_id = id;
         this.groupForm.name = dat.data.name;
         this.groupForm.listval = dat.data.permissions;
      }).catch(err=>{      
         console.log(err.response);
      });
    },
    submitForm(){
      this.axios.put(cons.apis + '/permission/groups/'+this.edit_id+'/', {
              "name": this.groupForm.name,
              "permissions": this.groupForm.listval,
            }, {
            headers: {
              'Authorization': 'JWT ' + token
            },
            responseType: 'json'           
        }).then(dat=>{
          this.$message({
            type: 'success',
            message: '修改组成功!'
          }); 
          this.pop_show = false;           
          this.resetForm('groupForm');
          this.$emit('fnResetTable');
        }).catch(err=>{
          console.log(err.response);
        })
    },
    fnDelGroup(id){
        this.edit_id = id;
        this.$confirm('此操作将删除该组, 是否继续?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          this.axios.delete(cons.apis + '/permission/groups/'+this.edit_id+'/',{
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
                  message:'组未找到！'
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
    resetForm(formName){
      this.$refs[formName].resetFields();
    }
  },
  mounted(){
    this.fnGetPowerList();
  }
}
</script>
