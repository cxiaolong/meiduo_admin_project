<template>
<div class="auther_table_wrap"> 
  <el-table
      :data="channels"
      border
      style="width:95.2%;margin:0px auto;" size="medium" >
      <el-table-column
        prop="id"
        label="id"
        width="100">
      </el-table-column>   
      <el-table-column
        prop="category"
        label="分类名">
      </el-table-column>
      <el-table-column
        prop="category_id"
        label="一级分类id">
      </el-table-column>
      <el-table-column
        prop="group"
        label="组名">
      </el-table-column>
      <el-table-column
        prop="group_id"
        label="组id">
      </el-table-column>
      <el-table-column
        prop="sequence"
        label="展示顺序">
      </el-table-column>
      <el-table-column
        prop="url"
        label="频道地址"
        width="160">
      </el-table-column>
      <el-table-column
      label="操作"
      width="160">
        <template slot-scope="scope">
          <el-button
            size="mini"
            @click="fnPopShow(scope.row.id)">编辑</el-button>
          <el-button
            size="mini"
            type="danger"
            @click="fnDelChannel(scope.row.id)">删除</el-button>
        </template>
      </el-table-column>
   </el-table>

    <el-dialog title="修改频道" :visible.sync="pop_show" append-to-body>
        <el-form :model="ChannelsForm" status-icon :rules="rulesChannelsForm" ref="ChannelsForm" label-width="100px">
          <el-form-item label="频道组：" prop="group_id">
            <el-select v-model="ChannelsForm.group_id" size="small">
              <el-option
                v-for="item in group_type_list"
                :key="item.id"
                :label="item.name"
                :value="item.id">
              </el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="一级分类：" prop="category_id">
            <el-select v-model="ChannelsForm.category_id" size="small">
              <el-option
                v-for="item in category_list"
                :key="item.id"
                :label="item.name"
                :value="item.id">
              </el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="频道地址：" prop="url">
            <el-input type="text" v-model="ChannelsForm.url" autocomplete="off" size="small"></el-input>
          </el-form-item>
          <el-form-item label="展示顺序：" prop="sequence">
            <el-input type="text" v-model="ChannelsForm.sequence" autocomplete="off" size="small"></el-input>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="submitForm">提交</el-button>
            <el-button @click="resetForm('ChannelsForm')">重置</el-button>
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
  props:['channels'],
   data () { 
    return {
      pop_show:false,
      group_type_list:[],
      category_list:[],
      ChannelsForm:{
        group_id:'',
        category_id:'',
        url:'',
        sequence:''
      },
      rulesChannelsForm:{
      }
    }
  },
  methods:{
  	fnPopShow(id){
  		this.pop_show = true;
      this.edit_id = id;
      this.axios.get(cons.apis + '/goods/channels/'+this.edit_id+'/', {
            headers: {
              'Authorization': 'JWT ' + token
            },
            responseType: 'json',
        })
        .then(dat=>{
            console.log(dat);
            this.ChannelsForm.group_id = dat.data.group_id;
            this.ChannelsForm.category_id = dat.data.category_id;
            this.ChannelsForm.url = dat.data.url;
            this.ChannelsForm.sequence = dat.data.sequence;
        }).catch(err=>{
           console.log(err.response);
      });
  	},
  	submitForm(){
  		this.axios.put(cons.apis + '/goods/channels/'+this.edit_id+'/', {
             "group_id": this.ChannelsForm.group_id,
              "category_id": this.ChannelsForm.category_id,
              "url": this.ChannelsForm.url,
              "sequence": this.ChannelsForm.sequence
            }, {
            headers: {
              'Authorization': 'JWT ' + token
            },
            responseType: 'json'           
        }).then(dat=>{
          this.$message({
            type: 'success',
            message: '频道修改成功!'
          }); 
        	this.pop_show = false;           
          this.resetForm('ChannelsForm');
          this.$emit('fnResetTable');
        }).catch(err=>{
        	console.log(err.response);
        })
  	},
  	fnDelChannel(id){
        this.edit_id = id;
        this.$confirm('此操作将删除该频道, 是否继续?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          this.axios.delete(cons.apis + '/goods/channels/'+this.edit_id+'/',{
              headers: {
                'Authorization': 'JWT ' + token
              },
              responseType:'json'           
          }).then(dat=>{
            this.$message({
              type: 'success',
              message: '删除频道成功!'
            });
            this.$emit('fnResetTable');
          }).catch(err=>{
            if(err.response.status==404){
               this.$message({
                  type:'info',
                  message:'频道未找到！'
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
    fnGetChannelType(){
      this.axios.get(cons.apis + '/goods/channel_types/', {
        headers: {
          'Authorization': 'JWT ' + token
        },
        responseType: 'json',
      })
      .then(dat=>{
          this.group_type_list = dat.data;        
      }).catch(err=>{      
         console.log(err.response);
      });
    },
    fnGetCategories(){
      this.axios.get(cons.apis + '/goods/categories/', {
        headers: {
          'Authorization': 'JWT ' + token
        },
        responseType: 'json',
      })
      .then(dat=>{
          this.category_list = dat.data;        
      }).catch(err=>{      
         console.log(err.response);
      });
    },
    resetForm(formName){
      this.$refs[formName].resetFields();
    }
  },
  mounted(){
    this.fnGetChannelType();
    this.fnGetCategories();
  }
}
</script>

<style scope>
.el-table th,.el-table td{
  text-align:center;
}
</style>
