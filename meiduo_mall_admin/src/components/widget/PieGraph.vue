<template>
  <div class="pannel02">
    <div id="pie_show" class="pie_show"></div>
  </div>
</template>

<script>
import cons from '@/components/constant'
export default {
  name: 'PieGraph',
  data () {
    return {
      msg: 'Welcome to Your Vue.js App'
    }
  },
  mounted(){
    let token = localStorage.token;
    let oPie = this.echarts.init(document.getElementById('pie_show'));
    let pro01 = new Promise((resolve,reject)=>{
        this.axios.get(cons.apis + '/statistical/day_active/', {
              headers: {
                'Authorization': 'JWT ' + token
              },
              responseType: 'json',
          })
          .then(dat=>{
              resolve(dat);
          }).catch(err=>{
             reject(dat);
        });
    });

    let pro02 = new Promise((resolve,reject)=>{
        this.axios.get(cons.apis + '/statistical/day_orders/', {
              headers: {
                'Authorization': 'JWT ' + token
              },
              responseType: 'json',
          })
          .then(dat=>{
              resolve(dat);
          }).catch(err=>{
             reject(dat);
        });
    });

    async function fnFinish(){
      let rs01 = await pro01;
      let rs02 = await pro02;
      //console.log([rs01,rs02]);

      var oPieopt =  
        {
          title : {
              top:10,
              text: '日活及下单用户比',
              x:'center'
          },
          tooltip : {
              trigger: 'item',
              formatter: "{a} <br/>{b} : {c} ({d}%)"
          },
          color:['#ffcb5b','#ff6666'],
          legend: {
              x : 'center',
              top:65,
              data:['日活用户','下单用户']
          },
          toolbox: {
              show : true,
              x : 'center',
              top:35,
              feature : {
                  mark : {show: true},
                  dataView : {show: true, readOnly: false},
                  magicType : {
                      show: true, 
                      type: ['pie', 'funnel'],
                      option: {
                          funnel: {
                              x: '25%',
                              width: '50%',
                              funnelAlign: 'left',
                              max: 1548
                          }
                      }
                  },
                  restore : {show: true},
                  saveAsImage : {show: true}
              }
          },
          calculable : true,
          series : [
              {
                  name:'访问来源',
                  type:'pie',
                  radius : '55%',
                  center: ['50%', '60%'],
                  data:[
                      {value:rs01.data.count, name:'日活用户'},
                      {value:rs02.data.count, name:'下单用户'},                   
                  ]
              }
          ]
      };

      oPie.setOption(oPieopt);
    }

    fnFinish();    
  }
}
</script>

<style scoped>
.pannel02{
  width:27.8%;
  height:350px;
  margin:20px auto 0;
  background-color:#fff;
  float:left;
  margin-left:2.4%;
}
.pie_show{
  width:100%;
  height:350px;
}
</style>
