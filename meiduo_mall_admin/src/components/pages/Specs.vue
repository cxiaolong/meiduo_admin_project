<template>
  <div class="specs_wrap">
    <BreadCrumb crumb="商品规格管理"></BreadCrumb>  
    <div class="top_bar">
       <AddSpecs @fnResetTable="fnGetData(1)"></AddSpecs>       
    </div>
    <SpecsTable :specs="aSpecsList" @fnResetTable="fnGetData(1)"></SpecsTable>
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
import AddSpecs from '@/components/widget/AddSpecs'
import SpecsTable from '@/components/widget/SpecsTable'
import cons from '@/components/constant'

export default {
  name: 'Specs',
  data () {
    return {
      page:1,
      pages:8,
      pagesize:10,
      aSpecsList:[]
    }
  },
  components:{
    BreadCrumb,
    AddSpecs,
    SpecsTable
  },
  mounted(){
    this.fnGetData(1);
  },
  methods:{
    fnGetData:function(num){
      let token = localStorage.token;
      this.axios.get(cons.apis + '/goods/specs/', {
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
          this.aSpecsList = dat.data.lists;
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
