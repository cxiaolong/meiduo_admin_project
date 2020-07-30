<template>
  <div class="brands_wrap">
    <BreadCrumb crumb="品牌管理"></BreadCrumb>  
    <div class="top_bar">
       <Addbrands @fnResetTable="fnGetData"></Addbrands>       
    </div>
    <BrandsTable :brands="aBrandsList" @fnResetTable="fnGetData"></BrandsTable>
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
import Addbrands from '@/components/widget/AddBrands'
import BrandsTable from '@/components/widget/BrandsTable'
import cons from '@/components/constant'

export default {
  name: 'Brands',
  data () {
    return {
      page:1,
      pages:8,
      pagesize:10,
      aBrandsList:[]
    }
  },
  components:{
    BreadCrumb,
    Addbrands,
    BrandsTable
  },
  mounted(){
    this.fnGetData(1);
  },
  methods:{
    fnGetData:function(num){
      let token = localStorage.token;
      this.axios.get(cons.apis + '/goods/brands/', {
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
          this.aBrandsList = dat.data.lists;
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
