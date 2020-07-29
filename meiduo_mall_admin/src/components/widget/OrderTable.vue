<template>
	<el-table
	    :data="orders"
	    border
	    style="width:95.2%;margin:0px auto;" size="medium" >
	    <el-table-column
	      prop="order_id"
	      label="订单id">
	    </el-table-column>
	    <el-table-column
	      prop="create_time"
	      label="创建时间">
	    </el-table-column>
	    <el-table-column
	      label="操作">
	        <template slot-scope="scope">
	          <el-button size="mini">
               <router-link :to='{name:"OrderDetail",params:{sEdit_id:scope.row.order_id}}'>订单详情</router-link>
            </el-button>
	        </template>
	    </el-table-column>
	 </el-table>
</template>

<script>
export default {
  name: 'OrderTable',
  props:['orders'],
  data () {
    return {
    }
  }
}
</script>

<style scoped>
.el-button--default a{
  display:block;
  color:#606266;
  width:80px;
  line-height:42px;
  margin:-15px -20px;
}
</style>
