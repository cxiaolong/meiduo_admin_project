<template>
<ul class="menu">
	<li v-for="(item,i) in aList" @click="fnSetMenu([i,-1])">
		<router-link :to="item.url" class="level1" :class="(i==aNowMenu[0])?'current':''"><i class="fa" :class="aStylist[i]"></i>{{ item.name }}</router-link>
		<ul v-if="item.submenu.length>0" :class="(i==aNowMenu[0])?'current'+item.submenu.length:''">
			<li v-for="(subitem, j) in item.submenu" @click.stop="fnSetMenu([i,j])"><router-link :to="subitem.url"  :class="(j==aNowMenu[1])?'active':''"><i class="fa fa-circle-o"></i>{{subitem.name}}</router-link></li>
		</ul>
	</li>			
</ul>
</template>

<script>
export default {
  name: 'Menu',
  data () {
    return {
      aList: [
      	{'name':'首 页','url':'/home','submenu':[]},
      	{'name':'用户管理','url':'/home/user','submenu':[]},
      	{'name':'商品管理','url':'','submenu':[
      		{'name':'SKU管理','url':'/home/sku'},
      		{'name':'SPU管理','url':'/home/spu'},
      		{'name':'规格管理','url':'/home/specs'},
          {'name':'规格选项管理','url':'/home/options'},
          {'name':'频道管理','url':'/home/channels'},
          {'name':'品牌管理','url':'/home/brands'},
          {'name':'图片管理','url':'/home/pictures'},
      	]},
      	{'name':'订单管理','url':'/home/order','submenu':[]},
      	{'name':'系统管理','url':'','submenu':[
          {'name':'权限管理','url':'/home/author'},      		
      		{'name':'用户组管理','url':'/home/group'},
          {'name':'管理员管理','url':'/home/admin'}      		
      	]}
      ],
      aStylist:['fa-home fa-lg','fa-user fa-lg','fa-shopping-basket','fa-list-alt','fa-gear fa-lg','fa-key fa-lg','fa-newspaper-o','fa-address-card-o','fa-truck fa-lg'],
      aNowMenu:[0,0]
    }
  },
  methods:{
  	fnSetMenu:function(arr){     
  		this.aNowMenu = [arr[0],arr[1]];
  	},
    fnResetMenu:function(url){
      if(url=='/home'){
        this.fnSetMenu([0,0])
      }
      if(url=='/home/user'){
        this.fnSetMenu([1,0])
      }
      if(url=='/home/author'){
        this.fnSetMenu([4,0])
      }
      if(url=='/home/group'){
        this.fnSetMenu([4,1])
      }
      if(url=='/home/admin'){
        this.fnSetMenu([4,2])
      }
      if(url=='/home/sku'){
        this.fnSetMenu([2,0])
      }
      if(url=='/home/spu'){
        this.fnSetMenu([2,1])
      }
      if(url=='/home/spuadd'){
        this.fnSetMenu([2,1])
      }
      if(url=='/home/spuedit'){
        this.fnSetMenu([2,1])
      }
      if(url=='/home/specs'){
        this.fnSetMenu([2,2])
      }
      if(url=='/home/options'){
        this.fnSetMenu([2,3])
      }
      if(url=='/home/channels'){
        this.fnSetMenu([2,4])
      }
      if(url=='/home/brands'){
        this.fnSetMenu([2,5])
      }
      if(url=='/home/pictures'){
        this.fnSetMenu([2,6])
      }
      if(url=='/home/order'){
        this.fnSetMenu([3,0])
      }
      if(url=='/home/order_detail'){
        this.fnSetMenu([3,0])
      }
    }
  },
  watch:{
    $route(to,from){
      this.fnResetMenu(to.path);      
    }
  },
  mounted(){
    var starturl = this.$route.path;    
    this.fnResetMenu(starturl);    
  }
}
</script>

<style scoped>
.menu{
  width:210px;
  margin:0px auto;
}
.menu .level1,.menu li ul a{
  display:block;
  width:210px;
  line-height:40px;
  text-decoration:none;
  color:#fff;
  font-size:14px;
  text-indent:10px;     
}
.menu li ul a{
  font-size:14px;
  text-indent:20px;
  background-color:#252934;         
}
.menu li .level1:hover{
  background-color:#fb5557;
}
.menu li a.current{
  background-color:#fb5557;
}
.menu li ul{
  height:0px;
  overflow:hidden;
  transition:all 300ms ease;
}
.menu li ul.current1{
	height:40px;
}
.menu li ul.current2{
	height:80px;
}
.menu li ul.current3{
	height:120px;
}
.menu li ul.current4{
	height:160px;
}
.menu li ul.current7{
  height:280px;
}
.menu li ul li a:hover{
  color:#fb5557;
}
.menu li ul li a.active{
   color:#fb5557
}
.menu li .fa{
  margin-right:20px;
}
.menu li li .fa{
  margin-right:10px;
}
</style>
