<template>
<div class="home_wrap">
  <div class="header">
    <a href="#" class="logo"><img src="static/images/logo.png" alt="美多商城logo"></a>
    <a href="javascript:;" class="quit" @click="fnQuit"><i class="fa fa-power-off"></i>&nbsp;&nbsp;退出</a>
    <div class="user_info">
      <img src="static/images/person.png" alt="user">
      <span>欢迎 {{username}}</span>
    </div>
  </div>
  <div class="side_bar">
     <Menu></Menu>
  </div>
  <div class="main_body">
     <router-view/>
  </div>
</div>
</template>

<script>
import Menu from '@/components/widget/Menu'
export default {
  name: 'Home',
  data () {
    return {
      username:''
    }
  },
  components:{
    Menu
  },
  mounted(){
    let user = localStorage.username;    
    if(user==undefined)
    {
       this.$router.push({path:'/'});
       return;
    }
    this.username = user;
  },
  methods:{
    fnQuit:function(){
       sessionStorage.clear();
       localStorage.clear();
       this.$router.push({path:'/'});
    }
  }
}
</script>

<style scoped>
.header{
  width:100%;
  height:60px;
  overflow:hidden;
  background:linear-gradient(90deg,#f63c2f,#803af2);
  position:fixed;
  left:0px;
  top:0px;
}
.header .logo{
  float:left;
  margin:12px 0 0 10px;
}

.user_info{
  float:right;
}
.user_info img{
  float:left;
  margin:10px 15px 0px 0px;
}
.user_info span{
  font-size:14px;
  line-height:60px;
  color:#fff;
}
.header .quit{
  float:right;
  width:60px;
  line-height:40px;
  margin:10px 0px 0px 20px;
  color:#fff;
  font-size:14px;
}
.header .quit:hover{
  color:#fb5557;
}
.side_bar{
  position:fixed;
  width:210px;
  background:#3d4955;
  left:0px;
  top:60px;
  bottom:0px;
}
.main_body{
  position:fixed;
  background:#f9f9f9;
  left:210px;
  top:60px;
  right:0px;
  bottom:0px;
  overflow:auto
}

</style>
