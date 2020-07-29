<template>
	<div class="breadcrumb">
		当前位置：{{ crumb }}
	</div>
</template>

<script>
export default {
  name: 'BreadCrumb',
  props:['crumb'],
  data () {
    return {
    }
  }
}
</script>

<style scoped>
.breadcrumb{
  line-height:39px;
  font-size:14px;
  text-indent:20px;
  border-bottom:1px solid #ddd;
  background:#fff;
}
</style>
