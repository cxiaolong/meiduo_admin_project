<template>
  <div class="user_wrap">
    <BreadCrumb crumb="订单管理"></BreadCrumb>  
    <div class="top_bar">
        <el-row>
          <el-col :span="8">
            <el-input placeholder="请输入搜索内容" v-model="keyword" class="input-with-select" size="small">
              <el-button slot="append" icon="el-icon-search" @click="fnGetData(1)"></el-button>
            </el-input>
          </el-col>
        </el-row>             
    </div>    
    <OrderTable :orders="aOrderList"></OrderTable>
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
import OrderTable from '@/components/widget/OrderTable'
import cons from '@/components/constant'
let token = localStorage.token;

export default {
  name: 'User',
  data () {
    return {
      keyword:'',
      page:1,
      pages:8,
      pagesize:10,
      aOrderList:[]
    }
  },
  components:{
    BreadCrumb,
    OrderTable    
  },
  mounted(){
    this.fnGetData(1);
  },
  methods:{
    fnGetData:function(num){      
      this.axios.get(cons.apis + '/orders/', {
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
          this.aOrderList = dat.data.lists;
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
  },
  mounted(){
    this.fnGetData(1);
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
