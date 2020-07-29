<template>
	<div class="add_channels_wrap">
    <el-button type="primary" size="small" @click="pop_show = true" class="pull-right">新增频道</el-button>    
    <el-dialog title="新增频道" :visible.sync="pop_show" append-to-body>
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
  name: 'AddChannels',
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
    submitForm(){
        this.axios.post(cons.apis + '/goods/channels/', {
              "group_id": this.ChannelsForm.group_id,
              "category_id": this.ChannelsForm.category_id,
              "url": this.ChannelsForm.url,
              "sequence": this.ChannelsForm.sequence
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
                message: '频道添加成功!'
              }); 
              this.pop_show = false;           
              this.resetForm('ChannelsForm');
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
