<template>
	<form class="search_form">
	  <input type="text" :placeholder="placetip" class="input_txt" v-model="keyword">
	  <input type="button" value="搜 索" class="input_sub" @click="$emit('fnSetKey',keyword)">
	</form>
</template>

<script>
export default {
  name: 'SearchForm',
  props:['placetip'],
  data () {
    return {
      keyword:''
    }
  }
}
</script>

<style scoped>
.search_form{
  float:left;
  height:36px;
  margin:4px 10px 0 0;
}

.search_form .input_txt{
  float:left;
  margin:0px;
  width:298px;
  height:26px;
  border:1px solid #d0d0d0;
  border-radius:4px;
  outline:none;
  text-indent:10px; 
  }

.search_form .input_sub{
  float:left;
  margin:0px;
  margin-left:15px;
  width:100px;
  height:28px;
  border:0px;
  border-radius:4px;
  background:#fb5557;
  color:#fff;
  cursor:pointer;
}
.search_form .input_sub:hover{
  opacity:0.8
}
</style>
