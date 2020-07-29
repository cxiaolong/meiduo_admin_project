<template>
  <div class="user_wrap">
    <BreadCrumb crumb="订单管理>订单详情"></BreadCrumb>
    <div class="center_wrap">
      <div class="order_detail_title_con">
        <h1 class="order_detail_title">订单详情</h1>
        <router-link to="/home/order" class="order_back">返回</router-link>
      </div>
      <el-row class="order_line">
        <el-col :span="8">订单号：{{ oOrder.order_id }}</el-col>
        <el-col :span="8">时间：{{ oOrder.create_time }}</el-col>
        <el-col :span="8">用户：{{ oOrder.user }}</el-col>
      </el-row>
      <el-row class="order_line">
        <el-col :span="8">商品总数：{{ oOrder.total_count }}</el-col>
        <el-col :span="8">总价：{{ oOrder.total_amount }}</el-col>
        <el-col :span="8">运费：{{ oOrder.freight }}</el-col>
      </el-row>
      <el-row class="order_line">
        <el-col :span="8">付款方式：{{ oOrder.pay_method | paystyle }}</el-col>
        <el-col :span="8">状态：{{ oOrder.status | process }}&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<el-button size="mini" round @click="pop_show=true">修改状态</el-button></el-col>
      </el-row>
      <el-table :data="oOrder.skus"  border style="margin:20px auto 0px;" size="medium">
        <el-table-column label="商品图片" width="150">
           <template slot-scope="scope">
              <img :src="scope.row.sku.default_image" width="102">
            </template>
        </el-table-column>
        <el-table-column prop="sku.name" label="商品名称"></el-table-column>
        <el-table-column prop="price" label="商品价格"></el-table-column>
        <el-table-column prop="count" label="商品数量"></el-table-column>
      </el-table>
    </div>

    <el-dialog title="修改状态" :visible.sync="pop_show" append-to-body>
        <el-form :model="statusForm" status-icon ref="statusForm" label-width="100px">
          <el-form-item label="订单状态：" prop="status">
            <el-select v-model="statusForm.status" size="small">
              <el-option
                v-for="item in status_list"
                :key="item.id"
                :label="item.name"
                :value="item.id">
              </el-option>
            </el-select>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="submitForm">提交</el-button>
            <el-button @click="pop_show=false">取消</el-button>
          </el-form-item>
        </el-form>
    </el-dialog>
</div>
</template>

<script>
let token = localStorage.token
import cons from '@/components/constant'
import BreadCrumb from '@/components/widget/BreadCrumb'
export default {
  name: 'SpuAdd',
  data () {
    return {
      edit_id:'',
      oOrder:{},
      pop_show:false,
      statusForm:{
        status:''
      },
      status_list:[
        {id:1, name:"待支付"},
        {id:2, name:"待发货"},
        {id:3, name:"待收货"},
        {id:4, name:"待评价"},
        {id:5, name:"已完成"},
        {id:6, name:"已取消"}
      ]
    }
  },
  components:{
    BreadCrumb
  },
  methods:{
  fnGetThisDetail(){
      this.axios.get(cons.apis + '/orders/' + this.edit_id + '/', {
          headers: {
            'Authorization': 'JWT ' + token
          },
          responseType: 'json'
      })
      .then(dat=>{
          //console.log(dat);
          this.oOrder = dat.data;
          this.edit_id = dat.data.order_id;
          this.statusForm.status = dat.data.status;
      }).catch(err=>{
         console.log(err);
      });
    },
    submitForm(){
      this.axios.put(cons.apis + '/orders/'+this.edit_id+'/status/', {
              "status":this.statusForm.status
            }, {
            headers: {
              'Authorization': 'JWT ' + token
            },
            responseType: 'json'
        }).then(dat=>{
          this.$message({
            type: 'success',
            message: '修改状态成功!'
          });
          this.pop_show = false;
          this.fnGetThisDetail();
        }).catch(err=>{
          console.log(err.response);
        })
    }
  },
  mounted(){
    this.edit_id = this.$route.params.sEdit_id;
    this.fnGetThisDetail();
  },
  filters:{
    process:function(val){
      if(val==''){
        return;
      }
      if(val==1){
        return '待支付'
      }
      else if(val==2){
        return '待发货'
      }
      else if(val==3){
        return '待收货'
      }
      else if(val==4){
        return '待评价'
      }
      else if(val==5){
        return '已完成'
      }
      else{
        return '已取消'
      }
    },
    paystyle:function(val){
      if(val==''){
          return;
      }
      if(val==1){
          return '货到付款'
      }else{
          return '支付宝'
      }
    }
  }
}
</script>

<style scoped>
.center_wrap{
    width:95.2%;
    overflow:hidden;
    margin:10px auto 10px;
  }
.order_detail_title_con{
  overflow:hidden;
}
.order_detail_title{
  line-height: 24px;
  font-size: 18px;
  color: #303133;
  margin:10px 0px 20px;
  float:left;
}
.order_back{
  float:right;
  margin:10px 0px 20px;
  color:#666;
  font-size:14px;
}
.order_line{
  line-height:45px;
  border-bottom:1px solid #ddd;
  font-size:14px;
}
.order_box{
  line-height:40px;
  border:1px solid #ddd;
  font-size:14px;
  margin-top:-1px;
}
.order_box2{
  border:1px solid #ddd;
  font-size:14px;
  margin-top:-1px;
  padding:10px 0px;
}
.text-center{
  text-align:center;
}
.pt30{
  padding-top:30px;
}

</style>
