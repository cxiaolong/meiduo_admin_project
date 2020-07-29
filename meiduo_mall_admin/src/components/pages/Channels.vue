<template>
  <div class="channels_wrap">
    <BreadCrumb crumb="商品频道管理"></BreadCrumb>  
    <div class="top_bar">
       <Addchannels @fnResetTable="fnGetData"></Addchannels>       
    </div>
    <ChannelsTable :channels="aChannelsList" @fnResetTable="fnGetData"></ChannelsTable>
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
import Addchannels from '@/components/widget/AddChannels'
import ChannelsTable from '@/components/widget/ChannelsTable'
import cons from '@/components/constant'

export default {
  name: 'Channels',
  data () {
    return {
      page:1,
      pages:8,
      pagesize:10,
      aChannelsList:[]
    }
  },
  components:{
    BreadCrumb,
    Addchannels,
    ChannelsTable
  },
  mounted(){
    this.fnGetData(1);
  },
  methods:{
    fnGetData:function(num){
      let token = localStorage.token;
      this.axios.get(cons.apis + '/goods/channels/', {
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
          console.log(dat.data);
          this.aChannelsList = dat.data.lists;
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
