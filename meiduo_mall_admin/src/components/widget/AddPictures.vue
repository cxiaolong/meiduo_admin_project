<template>
	<div class="add_channels_wrap">
    <el-button type="primary" size="small" @click="pop_show = true" class="pull-right">新增商品图片</el-button>    
    <el-dialog title="新增商品图片" :visible.sync="pop_show" append-to-body>
        <el-form :model="PicturesForm" status-icon :rules="rulesBrandsForm" ref="BrandsForm" label-width="100px">
          <el-form-item label="SKU商品id：" prop="content_type">
            <el-select v-model="PicturesForm.sku" size="small">
              <el-option
                v-for="item in sku_list"
                :key="item.id"
                :label="item.name"
                :value="item.id">
              </el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="商品图片" prop="logo">
            <el-upload 
            action=""
            :auto-upload="false">
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
      sku_list:[],
      PicturesForm:{
        sku:'',
        image:'',
      },
      rulesBrandsForm:{
      }
    }
  },
  methods:{
    submitForm(){
        let fileValue = document.querySelector('.el-upload .el-upload__input');
        let fd = new FormData();
        fd.append('sku', this.PicturesForm.sku);
        fd.append('image', fileValue.files[0], fileValue.files[0].name);

        this.axios.post(cons.apis + '/skus/images/', fd, {
            headers: {
              'Authorization': 'JWT ' + token,
              'Content-Type':'multipart/form-data'
            },
            responseType: 'json'           
        })
        .then(dat=>{
            console.log(dat);
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
    fnGetSkuList(){
      this.axios.get(cons.apis + '/skus/simple/', {
        headers: {
          'Authorization': 'JWT ' + token
        },
        responseType: 'json',
      })
      .then(dat=>{
          console.log(dat.data);
          this.sku_list = dat.data;        
      }).catch(err=>{      
         console.log(err.response);
      });
    },
    resetForm(formName){
      this.$refs[formName].resetFields();
    }
  },
  mounted(){
    this.fnGetSkuList();
  }
}
</script>
