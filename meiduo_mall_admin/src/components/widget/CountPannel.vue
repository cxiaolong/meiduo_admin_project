<template>
<div class="spannels">
	<div class="spannel scolor01">
		<em>{{total_count}}</em><span>人</span>
		<b>用户总数</b>
	</div>
	<div class="spannel scolor02">
		<em>{{day_increment}}</em><span>人</span>
		<b>日增用户</b>
	</div>
	<div class="spannel scolor03">
		<em>{{day_active}}</em><span>人</span>
		<b>日活用户</b>
	</div>
	<div class="spannel scolor04">
		<em>{{day_orders}}</em><span>人</span>
		<b>下单用户</b>
	</div>		
</div>
</template>

<script>
import cons from '@/components/constant'
export default {
  name: 'CountPannel',
  data(){
    return {
      total_count:0,
      day_increment:0,
      day_active:0,
      day_orders:0
    }
  },
  mounted(){
    let token = localStorage.token;

    // 获取总人数
    this.axios.get(cons.apis + '/statistical/total_count/', {
        headers: {
          'Authorization': 'JWT ' + token
        },
        responseType: 'json',
    })
    .then(dat=>{
        console.log(dat);
        this.total_count = dat.data.count;

    }).catch(err=>{
       console.log(err.response);      
       if(err.response.status==401){
          this.$router.push({path:'/'});
       }
    });

    // 获取日增人数
    this.axios.get(cons.apis + '/statistical/day_increment/', {
        headers: {
          'Authorization': 'JWT ' + token
        },
        responseType: 'json',
    })
    .then(dat=>{
        this.day_increment = dat.data.count;
    }).catch(err=>{
       console.log(err);
    });

    // 获取日活人数
    this.axios.get(cons.apis + '/statistical/day_active/', {
        headers: {
          'Authorization': 'JWT ' + token
        },
        responseType: 'json',
    })
    .then(dat=>{
        this.day_active = dat.data.count;
    }).catch(err=>{
       console.log(err);
    });

    // 获取下单人数
    this.axios.get(cons.apis + '/statistical/day_orders/', {
        headers: {
          'Authorization': 'JWT ' + token
        },
        responseType: 'json',
    })
    .then(dat=>{
        this.day_orders = dat.data.count;
    }).catch(err=>{
       console.log(err);
    });
  }
}
</script>

<style scoped>
.spannel{
  width:22%;
  float:left;
  margin-left:2.4%;
  height:100px;
  overflow:hidden;
  text-align:center;
  position:relative;
}
.spannel em{
  font-size:50px;
  line-height:50px;
  display:inline-block;
  margin:10px 0 0 20px;
  font-family:'Arial';
  color:rgba(255,255,255,0.8);
}
.spannel span{
  font-size:14px;
  display:inline-block;
  color:rgba(255,255,255,0.8);
  margin-left:10px;
}
.spannel b{
  position:absolute;
  left:0;
  bottom:0;
  width:100%;
  line-height:24px;
  background:rgba(0,0,0,0.1);
  color:#fff;
  font-size:14px;
  font-weight:normal;
}
.scolor01{
  background-color:#ff9565;
}
.scolor02{
  background-color:#9ed367;
}
.scolor03{
  background-color:#23b7e5;
}
.scolor04{
  background-color:#dd74f4;
}
.spannels{
  overflow:hidden;
  margin:20px auto 0;
}
</style>
