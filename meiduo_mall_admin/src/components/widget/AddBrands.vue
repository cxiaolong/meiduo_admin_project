<template>
	<div class="add_channels_wrap">
    <el-button type="primary" size="small" @click="pop_show = true" class="pull-right">新增品牌</el-button>    
    <el-dialog title="新增品牌" :visible.sync="pop_show" append-to-body>
        <el-form :model="BrandsForm" status-icon :rules="rulesBrandsForm" ref="BrandsForm" label-width="100px">
          <el-form-item label="品牌名称：" prop="name">
            <el-input type="text" v-model="BrandsForm.name" autocomplete="off" size="small"></el-input>
          </el-form-item>
          <el-form-item label="品牌首字母：" prop="first_letter">
            <el-input type="text" v-model="BrandsForm.first_letter" autocomplete="off" size="small"></el-input>
          </el-form-item>
          <el-form-item label="logo图片" prop="logo">
            <el-upload 
            action=""
            :auto-upload="false"
            >
            <el-button size="small" type="primary">点击选择图片</el-button>
            </el-upload>
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
      BrandsForm:{
        name:'',
        first_letter:'',
      },
      fileList:[],
      rulesBrandsForm:{
      }
    }
  },
  methods:{
    submitForm(){
        let fileValue = document.querySelector('.el-upload .el-upload__input');
        let fd = new FormData();

        fd.append('name', this.BrandsForm.name);
        fd.append('first_letter', this.BrandsForm.first_letter);
        fd.append('logo', fileValue.files[0], fileValue.files[0].name);
        this.axios.post(cons.apis + '/goods/brands/', fd, {
            headers: {
              'Authorization': 'JWT ' + token,
              'Content-Type':'multipart/form-data'
            },
            responseType: 'json'           
        })
        .then(dat=>{
            if(dat.status==201){
              this.$message({
                type: 'success',
                message: '品牌添加成功!'
              }); 
              this.pop_show = false;
              this.$emit('fnResetTable');            
              this.resetForm('ChannelsForm');                                     
            }
        }).catch(err=>{
            console.log(err.response);
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
