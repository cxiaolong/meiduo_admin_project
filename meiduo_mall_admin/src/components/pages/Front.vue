<template>
  <div class="front_wrap">
    <BreadCrumb crumb="首页"></BreadCrumb>
    <CountPannel></CountPannel>
    <CurveGraph></CurveGraph>
    <PieGraph></PieGraph>
    <ColumnGraph></ColumnGraph>
  </div>
</template>

<script>
import BreadCrumb from '@/components/widget/BreadCrumb'
import CountPannel from '@/components/widget/CountPannel'
import CurveGraph from '@/components/widget/CurveGraph'
import PieGraph from '@/components/widget/PieGraph'
import ColumnGraph from '@/components/widget/ColumnGraph'
export default {
  name: 'Front',
  data () {
    return {
    }
  },
  components:{
    BreadCrumb,
    CountPannel,
    CurveGraph,
    PieGraph,
    ColumnGraph
  },
  mounted(){
   
  },
  methods:{
   
  }
}
</script>