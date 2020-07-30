<template>
  <div class="options_wrap">
    <BreadCrumb crumb="规格选项管理"></BreadCrumb>  
    <div class="top_bar">
       <AddOptions @fnResetTable="fnGetData"></AddOptions>       
    </div>
    <OptionsTable :options="aOptionsList" @fnResetTable="fnGetData"></OptionsTable>
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
import AddOptions from '@/components/widget/AddOptions'
import OptionsTable from '@/components/widget/OptionsTable'
import cons from '@/components/constant'

export default {
  name: 'Specs',
  data () {
    return {
      page:1,
      pages:8,
      pagesize:10,
      aOptionsList:[]
    }
  },
  components:{
    BreadCrumb,
    AddOptions,
    OptionsTable
  },
  mounted(){
    this.fnGetData(1);
  },
  methods:{
    fnGetData:function(num){
      let token = localStorage.token;
      this.axios.get(cons.apis + '/specs/options/', {
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
          this.aOptionsList = dat.data.lists;
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
