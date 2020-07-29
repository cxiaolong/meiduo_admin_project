<template>
<div class="auther_table_wrap"> 
  <el-table
      :data="brands"
      border
      style="width:95.2%;margin:0px auto;" size="medium" >
      <el-table-column
        prop="id"
        label="id"
        width="100">
      </el-table-column>   
      <el-table-column
        prop="name"
        label="品牌名称">
      </el-table-column>
      <el-table-column
        label="logo图片地址">
        <template slot-scope="scope">
            <img :src="scope.row.logo" width="102">
        </template>
      </el-table-column>
      <el-table-column
        prop="first_letter"
        label="品牌首字母">
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
            @click="fnDelBrands(scope.row.id)">删除</el-button>
        </template>
      </el-table-column>
   </el-table>

    <el-dialog title="修改品牌" :visible.sync="pop_show" append-to-body>
        <el-form :model="BrandsForm" status-icon :rules="rulesBrandsForm" ref="ChannelsForm" label-width="100px">
          <el-form-item label="品牌名称：" prop="name">
            <el-input type="text" v-model="BrandsForm.name" autocomplete="off" size="small"></el-input>
          </el-form-item>
          <el-form-item label="品牌首字母：" prop="first_letter">
            <el-input type="text" v-model="BrandsForm.first_letter" autocomplete="off" size="small"></el-input>
          </el-form-item>
          <el-form-item label="logo图片" prop="logo">
            <template slot-scope="scope">
                <img :src="BrandsForm.logo" width="102">
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
  props:['brands'],
   data () { 
    return {
      pop_show:false,
      group_type_list:[],
      category_list:[],
      BrandsForm:{
        name:'',
        first_letter:'',
        logo:''
      },
      fileList:[],
      rulesBrandsForm:{
      }
    }
  },
  methods:{
  	fnPopShow(id){
  		this.pop_show = true;
      this.edit_id = id;
      this.axios.get(cons.apis + '/goods/brands/'+this.edit_id+'/', {
            headers: {
              'Authorization': 'JWT ' + token
            },
            responseType: 'json',
        })
        .then(dat=>{
           this.BrandsForm.name = dat.data.name;
           this.BrandsForm.logo = dat.data.logo;
           this.BrandsForm.first_letter = dat.data.first_letter;
        }).catch(err=>{
           console.log(err.response);
      });
  	},
  	submitForm(){
      let fileValue = document.querySelector('.el-upload .el-upload__input');
      let fd = new FormData();

      fd.append('name', this.BrandsForm.name);
      fd.append('first_letter', this.BrandsForm.first_letter);
      fd.append('logo', fileValue.files[0], fileValue.files[0].name);

  		this.axios.put(cons.apis + '/goods/brands/'+this.edit_id+'/', fd, {
            headers: {
              'Authorization': 'JWT ' + token
            },
            responseType: 'json'           
        }).then(dat=>{
          this.$message({
            type: 'success',
            message: '品牌修改成功!'
          }); 
        	this.pop_show = false;           
          this.resetForm('ChannelsForm');
          this.$emit('fnResetTable');
        }).catch(err=>{
        	console.log(err.response);
        })
  	},
  	fnDelBrands(id){
        this.edit_id = id;
        this.$confirm('此操作将删除该品牌, 是否继续?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          this.axios.delete(cons.apis + '/goods/brands/'+this.edit_id+'/',{
              headers: {
                'Authorization': 'JWT ' + token
              },
              responseType:'json'           
          }).then(dat=>{
            this.$message({
              type: 'success',
              message: '删除品牌成功!'
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
