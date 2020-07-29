<template>
  <div class="pannel03">
    <div id="column_show" class="column_show"></div>
  </div>
</template>

<script>
import cons from '@/components/constant'
export default {
  name: 'ColumnGraph',
  data () {
    return {
    }
  },
  mounted(){
     let token = localStorage.token;

    // 获取商品访问量
    this.axios.get(cons.apis + '/statistical/goods_day_views/', {
        headers: {
          'Authorization': 'JWT ' + token
        },
        responseType: 'json',
    }).then(dat=>{
        //console.log(dat.data);
        let aList_all = dat.data;
        let aCategory = [];
        let aCount = [];

        for(var i=0;i<aList_all.length;i++){
            aCategory.push(aList_all[i].category);
            aCount.push(aList_all[i].count);
        }

        var oColumn = this.echarts.init(document.getElementById('column_show'));
        var oColumnopt =  
              {
                title:{
                    text: '商品访问量',
                    left: 'center',
                    top: '10'
              },
                tooltip : {
                    trigger: 'axis'
                },
                legend: {
                    data:['访问量'],
                    top:'40'          
                },
                toolbox: {
                    show : true,
                    feature : {
                        mark : {show: true},
                        dataView : {show: true, readOnly: false},
                        magicType : {show: true, type: ['line', 'bar']},
                        restore : {show: true},
                        saveAsImage : {show: true}
                    }
                },
                calculable : true,
                xAxis : [
                    {
                        type : 'category',
                        data : aCategory
                    }
                ],
                yAxis : [
                    {
                        name : '访问量',
                        type : 'value'
                    }
                ],
                series : [
                    {
                        name:'访问量',
                        type:'bar',
                        barWidth:30, 
                        itemStyle:{
                           normal: {areaStyle: {type: 'default'}, color: '#f77476'}
                        },
                        data:aCount
                    }
                ],
                grid: {
                    show: true,             
                    x:50,
                    x2:50,
                    y:80,
                    height:260
                },
                dataZoom: [//给x轴设置滚动条
                 {
                     start:0,//默认为0
                     end: 100-1000/31,//默认为100
                     type: 'slider',
                     show: true,
                     xAxisIndex: [0],
                     handleSize: 0,//滑动条的 左右2个滑动条的大小
                     height:8,//组件高度
                     left:45, //左边的距离
                     right:50,//右边的距离
                     bottom: 26,//右边的距离
                     handleColor: '#ddd',//h滑动图标的颜色
                     handleStyle: {
                         borderColor: "#cacaca",
                         borderWidth: "1",
                         shadowBlur: 2,
                         background: "#ddd",
                         shadowColor: "#ddd",
                     }
                  }]
            };
            oColumn.setOption(oColumnopt);



    }).catch(err=>{
       console.log(err);
    });   
  }
}
</script>

<style scoped>
.pannel03{
  width:95.2%;
  overflow:hidden;
  margin:20px auto 0;
  background-color:#fff;
  float:left;
  margin-left:2.4%;
}
.column_show{
  width:100%;
  height:400px;
}
</style>
