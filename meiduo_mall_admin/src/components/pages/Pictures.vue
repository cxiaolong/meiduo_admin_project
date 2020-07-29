<template>
  <div class="pictures_wrap">
    <BreadCrumb crumb="商品图片管理"></BreadCrumb>  
    <div class="top_bar">
       <Addpictures @fnResetTable="fnGetData"></Addpictures>       
    </div>
    <PicturesTable :pictures="aPicturesList" @fnResetTable="fnGetData"></PicturesTable>
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
import Addpictures from '@/components/widget/AddPictures'
import PicturesTable from '@/components/widget/PicturesTable'
import cons from '@/components/constant'

export default {
  name: 'Brands',
  data () {
    return {
      page:1,
      pages:8,
      pagesize:10,
      aPicturesList:[]
    }
  },
  components:{
    BreadCrumb,
    Addpictures,
    PicturesTable
  },
  mounted(){
    this.fnGetData(1);
  },
  methods:{
    fnGetData:function(num){
      let token = localStorage.token;
      this.axios.get(cons.apis + '/skus/images/', {
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
          this.aPicturesList = dat.data.lists;
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
