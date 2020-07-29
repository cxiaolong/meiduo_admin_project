<template>
<div class="sku_con">
	<el-table :data="spus" border style="width:95.2%;margin:0px auto;" size="medium" >
	    <el-table-column prop="id" label="id" width="100"></el-table-column>
	    <el-table-column prop="name" label="SPU名称"></el-table-column>
	    <el-table-column prop="brand" label="品牌名称"></el-table-column>
	    <el-table-column prop="brand_id" label="品牌id"></el-table-column>
      <el-table-column prop="category1_id" label="一级分类id"></el-table-column>
      <el-table-column prop="category2_id" label="二级分类id"></el-table-column>
      <el-table-column prop="category3_id" label="三级分类id"></el-table-column>
      <el-table-column prop="sales" label="SPU商品销量"></el-table-column>
      <el-table-column prop="comments" label="SPU商品评论量"></el-table-column> 
      <el-table-column
	      label="操作">
	        <template slot-scope="scope">
	          <el-button size="mini">
               <router-link :to='{name:"SpuEdit",params:{sEdit_id:scope.row.id}}'>修改</router-link>
            </el-button>
	          <el-button
	            size="mini"
	            type="danger"
	            @click="fnDelSpu(scope.row.id)">删除</el-button>
	        </template>
	    </el-table-column>
	 </el-table>	
</div>
</template>

<script>
import cons from '@/components/constant';
let token = localStorage.token;
export default {
  name: 'SkuTable',
  props:['spus'],
  data () {       
    return {
      edit_id:''
    }
  },
  methods:{
    fnDelSpu(id){
        this.edit_id = id;
        this.$confirm('此操作将删除该SPU, 是否继续?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          this.axios.delete(cons.apis + '/goods/'+this.edit_id+'/',{
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
                  message:'商品未找到！'
               });
            }
          })
        }).catch(() => {
          this.$message({
            type: 'info',
            message: '已取消删除'
          });          
        });     
    }
  }
}
</script>
<style>
	.el-button+.el-button{
		margin-left:0px;
		margin-top:10px;
	}
  .el-button--default a{
  display:block;
  color:#606266;
  width:65px;
  line-height:42px;
  margin:-15px -20px;

}
</style>
