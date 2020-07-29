<template>
	<div class="pagenation">
		<a href="javascript:;" v-if="nowpage!=1" @click="fnChangePage(1)">首页</a>
		<a href="javascript:;" v-if="nowpage!=1" @click="fnChangePage(nowpage-1)">上一页</a>
		<a href="javascript:;" v-for="item in pagelist" :class="[(item==nowpage)?'active':'']" @click="fnChangePage(item)">{{ item }}</a>		
		<a href="javascript:;" v-if="nowpage!=nowpages" @click="fnChangePage(nowpage+1)">下一页</a>
		<a href="javascript:;" v-if="nowpage!=nowpages" @click="fnChangePage(nowpages)">尾页</a>
	</div>
</template>

<script>
export default {
  name: 'Pagenation',
  props:['page','pages'],
  data(){
    return {
    	nowpage:0,
    	nowpages:0,
    	pagelist:[]
    }
  },
  methods:{
  	fnTellPage:function(n){
  		this.$emit('foParent', n);
  	},
  	fnSetpage:function(){
  		if(this.nowpage<4&&this.nowpages<=5)
  		{
  			var aList = [];
  			for(var i=1;i<=this.nowpages;i++){
  				aList.push(i);
  			}
  		}
  		else if(this.nowpage<4&&this.nowpages>5)
  		{
  			var aList = [1,2,3,4,5];
  		}
  		else if((this.nowpages-this.nowpage)>=2)
  		{
  			var aList = [this.nowpage-2,this.nowpage-1,this.nowpage,this.nowpage+1,this.nowpage+2];
  		}
  		else
  		{
  			aList = [this.nowpages-4,this.nowpages-3,this.nowpages-2,this.nowpages-1,this.nowpages]
  		}
  		this.pagelist = aList;
  	},
  	fnChangePage:function(iNum){
  		this.nowpage = iNum;
  		this.fnSetpage();
  		this.$emit('fnSetPage',iNum);
  	}
  },
  mounted(){
  	 this.nowpage = this.page;
  	 this.nowpages = this.pages;
  	 this.fnSetpage();
  },
  watch:{
  	page:function(){
  		this.nowpage = this.page;
  	 	this.nowpages = this.pages;
  	 	this.fnSetpage();
  	},
  	pages:function(){
  		this.nowpage = this.page;
  	 	this.nowpages = this.pages;
  	 	this.fnSetpage();
  	}
  } 
}
</script>

<style scoped>
.pagenation{
	width:100%;
	text-align:center;
	margin-top:15px;
}
.pagenation a{
	display:inline-block;
	font-size:12px;
	padding:3px 9px;
	background: #fff;
	border: 1px solid #c5b7b7;
	color: #888;
	margin: 0 2px;
	text-decoration: none;
}
.pagenation a:hover{
	border: 1px solid #fb5557;
	color:red;
}
.pagenation a.active{
	background:#fb5557;
	color:#fff;
	border:1px solid #fb5557;
}

</style>
