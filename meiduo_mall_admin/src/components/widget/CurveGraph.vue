<template>
  <div class="pannel01">
    <div id="curve_show" class="curve_show"></div>
  </div>
</template>

<script>
import cons from '@/components/constant'
export default {
  name: 'CurveGraph',
  data () {
    return {
    }
  },
  mounted(){
    let token = localStorage.token;

    // 获取月新增用户
    this.axios.get(cons.apis + '/statistical/month_increment/', {
        headers: {
          'Authorization': 'JWT ' + token
        },
        responseType: 'json',
    })
    .then(dat=>{
        let aList_all = dat.data;
        let aCount = [];
        let aDate = [];

        for(var i=0;i<aList_all.length;i++){
            aCount.push(aList_all[i].count);
            aDate.push(aList_all[i].date);
        }

        let oCurve = this.echarts.init(document.getElementById('curve_show'));
        let oCurveopt = 
                {
                  title:{
                      text: '月新增用户',
                      left: 'center',
                      top: '10'
                  },
                  tooltip:{
                      trigger: 'axis'
                  },
                  legend: {
                      data:['active'],
                      top: '40'
                  },
                  toolbox: {
                      show : true,
                      feature : {
                          mark : {show: true},
                          dataView : {show: true, readOnly: false},
                          magicType : {show: true, type: ['line','bar']},
                          restore : {show: true},
                          saveAsImage : {show: true}
                      }
                  },
                  calculable : true,               
                  xAxis : [
                      {
                          name: '日',
                          type : 'category',
                          boundaryGap : false,
                          data :aDate
                      }
                  ],        
                  yAxis : [
                      {
                          name: '月新增用户',
                          type : 'value'
                      }
                  ],      
                  series : [
                      {
                          name:'active',
                          type:'line',
                          smooth:true,
                          lineStyle: {color: '#f80'},
                          data:aCount,
                          areaStyle:{
                            normal:{
                                color: new this.echarts.graphic.LinearGradient(0, 0, 0, 1, [{
                                    offset: 0,
                                    color: 'rgba(255,136,0,0.39)'
                                }, {
                                    offset: 0.34,
                                    color: 'rgba(255,180,0,0.25)'
                                },{
                                    offset: 1,
                                    color: 'rgba(255,222,0,0.00)'
                                }])
                            }
                        }
                  }],
                  grid: {
                      show: true,             
                      x:50,
                      x2:50,
                      y:80,
                      height:220
                  }
                 
                };
              oCurve.setOption(oCurveopt);
        

    }).catch(err=>{
       console.log(err);
    });


    
  }
}
</script>

<style scoped>
.pannel01{
  width:65%;
  overflow:hidden;
  margin:20px auto 0;
  background-color:#fff;
  float:left;
  margin-left:2.4%;
}
.curve_show{
  width:100%;
  height:350px;
}
</style>
