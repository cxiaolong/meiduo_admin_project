<template>
	<div class="add_user_wrap">
    <el-button type="primary" size="small"  @click="pop_show = true">新增商品</el-button>
      <el-dialog title="新增商品" :visible.sync="pop_show" append-to-body width="60%">
        <el-form :model="skuForm" :inline="true" status-icon ref="userForm" label-width="100px">
          <el-form-item label="名称:" prop="name">
            <el-input type="text" v-model="skuForm.name" autocomplete="off" size="small"></el-input>
          </el-form-item>
          <el-form-item label="副标题:" prop="caption">
            <el-input type="text" v-model="skuForm.caption" autocomplete="off" size="small"></el-input>
          </el-form-item>
          <el-form-item label="价格:" prop="price">
            <el-input type="text" v-model="skuForm.price" autocomplete="off" size="small"></el-input>
          </el-form-item>
          <el-form-item label="进价:" prop="cost_price">
            <el-input type="text" v-model="skuForm.cost_price" autocomplete="off" size="small"></el-input>
          </el-form-item>
          <el-form-item label="市场价:" prop="market_price">
            <el-input type="text" v-model="skuForm.market_price" autocomplete="off" size="small"></el-input>
          </el-form-item>
          <el-form-item label="库存:" prop="stock">
            <el-input type="text" v-model="skuForm.stock" autocomplete="off" size="small"></el-input>
          </el-form-item>
          <el-form-item label="分类:" prop="category_id">
            <el-select v-model="skuForm.category_id" size="small">
              <el-option
                v-for="item in category_list"
                :key="item.id"
                :label="item.name"
                :value="item.id"
                >
              </el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="上下架:" prop="is_launched">
            <el-radio v-model="skuForm.is_launched" label="true">是</el-radio>
            <el-radio v-model="skuForm.is_launched" label="false">否</el-radio>
          </el-form-item>
          <el-form-item label="SPU" prop="spu_id">
            <el-select v-model="skuForm.spu_id" size="small" @change="skuForm.specs={}">
              <el-option
                v-for="item in goods_list"
                :key="item.id"
                :label="item.name"
                :value="item.id"
                >
              </el-option>              
            </el-select>
          </el-form-item>
          <el-form-item v-for="item in specs_list" :label="item.name" :key="item.id">
            <el-select v-model="skuForm.specs[item.id]" size="small">
              <el-option
                v-for="opt in item.options"
                :key="opt.id"
                :label="opt.value"
                :value="opt.id"
                >
              </el-option>
            </el-select>
          </el-form-item><br>
          <el-form-item>
            <el-button type="primary" @click="submitForm">提交</el-button>
            <el-button @click="resetForm">重置</el-button>
          </el-form-item>
        </el-form>
      </el-dialog>
	</div>  
</template>

<script>
import cons from '@/components/constant';
let token = localStorage.token;
export default {
  name: 'AddUser',
  data () {       
    return {
      pop_show:false,
      skuForm:{
        "name": '',
        "spu_id":'',
        "caption": '',
        "category_id": '',
        "price": '',
        "cost_price":'',
        "market_price":'',
        "stock": '',
        "is_launched":'',
        "specs":{}
      },
      category_list:[],
      goods_list:[],
      specs_list:[],
    }
  },
  methods:{  
    fnGetCategory(){
      this.axios.get(cons.apis + '/skus/categories/', {
        headers: {
          'Authorization': 'JWT ' + token
        },
        responseType: 'json',
      })
      .then(dat=>{
          this.category_list = dat.data;        
      }).catch(err=>{      
         console.log(err.response);
      });
    },
    fnGetGoods(){
      this.axios.get(cons.apis + '/goods/simple/', {
        headers: {
          'Authorization': 'JWT ' + token
        },
        responseType: 'json',
      })
      .then(dat=>{
          this.goods_list = dat.data;        
      }).catch(err=>{      
         console.log(err.response);
      });
    },
    fnGetSpecs(){
      this.axios.get(cons.apis + '/goods/'+ this.skuForm.spu_id + '/specs/', {
        headers: {
          'Authorization': 'JWT ' + token
        },
        responseType: 'json',
      })
      .then(dat=>{
          this.specs_list = dat.data;       
      }).catch(err=>{      
         console.log(err.response);
      });
    },
    submitForm(){
       var specs_sub_list = [];
       for(var k in this.skuForm.specs){
          specs_sub_list.push({'spec_id':k,'option_id':this.skuForm.specs[k]})
       }
       this.axios.post(cons.apis + '/skus/', {
              "name":this.skuForm.name,
              "spu_id":this.skuForm.spu_id,
              "caption":this.skuForm.caption,
              "category_id": this.skuForm.category_id,
              "price": this.skuForm.price,
              "cost_price": this.skuForm.cost_price,
              "market_price": this.skuForm.market_price,
              "stock": this.skuForm.stock,
              "is_launched": this.skuForm.is_launched,
              "specs":specs_sub_list
            },{
            headers: {
              'Authorization': 'JWT ' + token
            },
            responseType: 'json'           
        })
        .then(dat=>{
            if(dat.status==201){
              this.$message({
                type: 'success',
                message: '商品添加成功!'
              });
              this.pop_show = false;
              this.skuForm.name = '';
              this.skuForm.spu_id = '';
              this.skuForm.caption = '';
              this.skuForm.category_id = '';
              this.skuForm.price = '';
              this.skuForm.cost_price = '';
              this.skuForm.market_price = '';
              this.skuForm.stock = '';
              this.skuForm.is_launched = '';
              this.skuForm.specs ={};
              this.$emit('fnResetTable');                        
            }
        }).catch(err=>{
           if(err.response.status==400){
               this.$message({
                  type:'info',
                  message:err.response.data.name[0]
              });
           }          
        }); 
    },
    resetForm(){
      this.skuForm.name = '';
      this.skuForm.spu_id = '';
      this.skuForm.caption = '';
      this.skuForm.category_id = '';
      this.skuForm.price = '';
      this.skuForm.cost_price = '';
      this.skuForm.market_price = '';
      this.skuForm.stock = '';
      this.skuForm.is_launched = '';
      this.skuForm.specs ={};
    }
  },  
  computed:{
     look_good_id(){
       return this.skuForm.spu_id
     }
  },
  mounted(){
    this.fnGetCategory();
    this.fnGetGoods();
  },
  watch:{
    look_good_id(newVal,oldVal){
       this.fnGetSpecs();
    }
  }
}
</script>

<style scoped>
.input_width{
  width:450px;
}
</style>
