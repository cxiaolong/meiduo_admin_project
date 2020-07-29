<template>
	<el-table
	    :data="users"
	    border
	    style="width:95.2%;margin:0px auto;" size="medium" >
	    <el-table-column
	      prop="id"
	      label="id"
	      width="100">
	    </el-table-column>
	    <el-table-column
	      prop="username"
	      label="用户名">
	    </el-table-column>
	    <el-table-column
	      prop="mobile"
	      label="手机号">
	    </el-table-column>
	    <el-table-column
	      prop="email"
	      label="邮箱">
	    </el-table-column>
	 </el-table>
</template>

<script>
export default {
  name: 'UserTable',
  props:['users'],
  data () {
    return {
    }
  }
}
</script>
