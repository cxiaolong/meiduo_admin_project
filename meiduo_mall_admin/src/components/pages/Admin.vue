<template>
  <div class="group_wrap">
    <BreadCrumb crumb="管理员管理"></BreadCrumb>  
    <div class="top_bar">
       <AddAdmin @fnResetTable="fnGetData"></AddAdmin>       
    </div>
    <AdminTable :admins="aAdminList" @fnResetTable="fnGetData"></AdminTable>
    <el-pagination
      background
      layout="prev, pager, next"
      :page-count="pages"
      :current-page="page"
      style="text-align:center;margin-top:10px"
      @current-change="fnGetPage"
      >
    </el-pagination>
  </div>
</template>

<script>
import BreadCrumb from '@/components/widget/BreadCrumb'
import AddAdmin from '@/components/widget/AddAdmin'
import AdminTable from '@/components/widget/AdminTable'
import cons from '@/components/constant'
export default {
  name: 'Admin',
  data () {
    return {
      page:1,
      pages:8,
      pagesize:10,
      aAdminList:[]
    }
  },
  components:{
    BreadCrumb,
    AddAdmin,
    AdminTable
  },
  mounted(){
    this.fnGetData(1);
  },
  methods:{
    fnGetData:function(num){
      let token = localStorage.token;
      this.axios.get(cons.apis + '/permission/admins/', {
          headers: {
            'Authorization': 'JWT ' + token
          },
          responseType: 'json',
          params:{
            page:num,
            pagesize:this.pagesize
          }
      })
      .then(dat=>{
          this.aAdminList = dat.data.lists;
          this.page = dat.data.page;
          this.pages = dat.data.pages;
      }).catch(err=>{
         console.log(err);
      });
    },   
    fnGetPage:function(dat){
      this.page = dat;
      this.fnGetData(this.page);
    }
  }
}
</script>

<style scoped>
.top_bar{
    width:95.2%;
    overflow:hidden;
    margin:10px auto;
  }
</style>
