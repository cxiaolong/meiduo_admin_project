<template>
  <div class="user_wrap">
    <BreadCrumb crumb="用户管理"></BreadCrumb>  
    <div class="top_bar">
        <el-row>
          <el-col :span="8">
            <el-input placeholder="请输入搜索内容" v-model="keyword" class="input-with-select" size="small">
              <el-button slot="append" icon="el-icon-search" @click="fnGetData(1)"></el-button>
            </el-input>
          </el-col>
          <el-col :span="8" :offset="8"><AddUser @fnSetKey="fnGetKey" class="pull-right"></AddUser></el-col>
        </el-row>             
    </div>    
    <UserTable :users="aUserList"></UserTable>
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
import AddUser from '@/components/widget/AddUser'
import UserTable from '@/components/widget/UserTable'
import cons from '@/components/constant'

export default {
  name: 'User',
  data () {
    return {
      keyword:'',
      page:1,
      pages:8,
      pagesize:10,
      aUserList:[]
    }
  },
  components:{
    BreadCrumb,
    AddUser,
    UserTable    
  },
  mounted(){
    this.fnGetData(1);
  },
  methods:{
    fnGetData:function(num){
      let token = localStorage.token;
      this.axios.get(cons.apis + '/users/', {
          headers: {
            'Authorization': 'JWT ' + token
          },
          responseType: 'json',
          params:{
            page:num,
            pagesize:this.pagesize,
            keyword:this.keyword
          }
      })
      .then(dat=>{
          this.aUserList = dat.data.lists;
          this.page = dat.data.page;
          this.pages = dat.data.pages;
      }).catch(err=>{
         console.log(err);
      });
    },
    fnGetKey:function(dat){
       this.keyword = dat;
       this.fnGetData(1);
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
    margin:10px auto 10px;
  }
</style>
