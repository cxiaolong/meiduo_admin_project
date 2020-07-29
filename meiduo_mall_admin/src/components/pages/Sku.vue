<template>
  <div class="user_wrap">
    <BreadCrumb crumb="sku管理"></BreadCrumb>  
    <div class="top_bar">
        <el-row>
          <el-col :span="8">
            <el-input placeholder="请输入搜索内容" v-model="keyword" class="input-with-select" size="small">
              <el-button slot="append" icon="el-icon-search" @click="fnGetData(1)"></el-button>
            </el-input>
          </el-col>
          <el-col :span="8" :offset="8"><AddSku @fnSetKey="fnGetKey" class="pull-right"></AddSku></el-col>
        </el-row>             
    </div>    
    <SkuTable :skus="aSkuList" @fnResetTable="fnGetData(1)"></SkuTable>
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
import AddSku from '@/components/widget/AddSku'
import SkuTable from '@/components/widget/SkuTable'
import cons from '@/components/constant'

export default {
  name: 'Sku',
  data () {
    return {
      keyword:'',
      page:1,
      pages:8,
      pagesize:10,
      aSkuList:[]
    }
  },
  components:{
    BreadCrumb,
    AddSku,
    SkuTable    
  },
  mounted(){
    this.fnGetData(1);
  },
  methods:{
    fnGetData:function(num){
      let token = localStorage.token;
      this.axios.get(cons.apis + '/skus/', {
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
          this.aSkuList = dat.data.lists;
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
