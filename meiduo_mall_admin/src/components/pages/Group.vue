<template>
  <div class="group_wrap">
    <BreadCrumb crumb="用户组管理"></BreadCrumb>  
    <div class="top_bar">
       <AddGroup @fnResetTable="fnGetData"></AddGroup>       
    </div>
    <GroupTable :groups="aGroupList" @fnResetTable="fnGetData"></GroupTable>
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
import AddGroup from '@/components/widget/AddGroup'
import GroupTable from '@/components/widget/GroupTable'

import cons from '@/components/constant'

export default {
  name: 'Group',
  data () {
    return {
      page:1,
      pages:8,
      pagesize:10,
      aGroupList:[]
    }
  },
  components:{
    BreadCrumb,
    AddGroup,
    GroupTable
  },
  mounted(){
    this.fnGetData(1);
  },
  methods:{
    fnGetData:function(num){
      let token = localStorage.token;
      this.axios.get(cons.apis + '/permission/groups/', {
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
          //console.log(dat);
          this.aGroupList = dat.data.lists;
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
