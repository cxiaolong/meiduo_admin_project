<template>
  <div class="authority_wrap">
    <BreadCrumb crumb="权限管理"></BreadCrumb>  
    <div class="top_bar">
       <AddAuthor  @fnResetTable="fnGetData(1)"></AddAuthor>       
    </div>
    <AuthorityTable :authors="aAuthorList" @fnResetTable="fnGetData(1)"></AuthorityTable>
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
import AddAuthor from '@/components/widget/AddAuthor'
import AuthorityTable from '@/components/widget/AuthorityTable'

import cons from '@/components/constant'

export default {
  name: 'Authority',
  data () {
    return {
      page:1,
      pages:8,
      pagesize:10,
      aAuthorList:[]
    }
  },
  components:{
    BreadCrumb,
    AddAuthor,
    AuthorityTable
  },
  mounted(){
    this.fnGetData(1);
  },
  methods:{
    fnGetData:function(num){
      let token = localStorage.token;
      this.axios.get(cons.apis + '/permission/perms/', {
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
          this.aAuthorList = dat.data.lists;
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
