<template>
<div class="auther_table_wrap"> 
  <el-table
      :data="pictures"
      border
      style="width:95.2%;margin:0px auto;" size="medium" >
      <el-table-column
        prop="id"
        label="id"
        width="100">
      </el-table-column>   
      <el-table-column
        prop="sku"
        label="SKU商品id">
      </el-table-column>
      <el-table-column
        label="商品图片">
        <template slot-scope="scope">
            <img :src="scope.row.image" width="100" height="100">
        </template>
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
            @click="fnDelPictures(scope.row.id)">删除</el-button>
        </template>
      </el-table-column>
   </el-table>

    <el-dialog title="修改商品图片" :visible.sync="pop_show" append-to-body>
        <el-form :model="PicturesForm" status-icon :rules="rulesPicturesForm" ref="BrandsForm" label-width="100px">
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
          <el-form-item label="商品图片" prop="image">
            <template slot-scope="scope">
                <img :src="PicturesForm.image" width="102">
            </template>
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
  name: 'OptionsTable',
  props:['pictures'],
   data () { 
    return {
      pop_show:false,
      sku_list:[],
      PicturesForm:{
        sku:'',
        image:'',
      },
      rulesPicturesForm:{
      }
    }
  },
  methods:{
  	fnPopShow(id){
  		this.pop_show = true;
      this.edit_id = id;
      this.axios.get(cons.apis + '/skus/images/'+this.edit_id+'/', {
            headers: {
              'Authorization': 'JWT ' + token
            },
            responseType: 'json',
        })
        .then(dat=>{
           this.PicturesForm.sku = dat.data.sku;
           this.PicturesForm.image = dat.data.image;
        }).catch(err=>{
           console.log(err.response);
      });
  	},
  	submitForm(){
      let fileValue = document.querySelector('.el-upload .el-upload__input');
      let fd = new FormData();
      fd.append('sku', this.PicturesForm.sku);
      fd.append('image', fileValue.files[0], fileValue.files[0].name);

  		this.axios.put(cons.apis + '/skus/images/'+this.edit_id+'/', fd, {
            headers: {
              'Authorization': 'JWT ' + token
            },
            responseType: 'json'           
        }).then(dat=>{
          this.$message({
            type: 'success',
            message: '商品图片修改成功!'
          }); 
        	this.pop_show = false;
          this.$emit('fnResetTable');           
          this.resetForm('ChannelsForm');          
        }).catch(err=>{
        	console.log(err.response);
        })
  	},
  	fnDelPictures(id){
        this.edit_id = id;
        this.$confirm('此操作将删除该商品图片, 是否继续?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          this.axios.delete(cons.apis + '/skus/images/'+this.edit_id+'/',{
              headers: {
                'Authorization': 'JWT ' + token
              },
              responseType:'json'           
          }).then(dat=>{
            this.$message({
              type: 'success',
              message: '删除图片成功!'
            });
            this.$emit('fnResetTable');
          }).catch(err=>{
            if(err.response.status==404){
               this.$message({
                  type:'info',
                  message:'图片未找到！'
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

<style scope>
.el-table th,.el-table td{
  text-align:center;
}
</style>
