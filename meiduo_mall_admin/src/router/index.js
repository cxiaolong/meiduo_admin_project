import Vue from 'vue'
import Router from 'vue-router'
import Login from '@/components/pages/Login'
import Home from '@/components/pages/Home'
import Front from '@/components/pages/Front'
import User from '@/components/pages/User'
import NotFound from '@/components/pages/NotFound'
import Authority from '@/components/pages/Authority'
import Group from '@/components/pages/Group'
import Admin from '@/components/pages/Admin'
import Sku from '@/components/pages/Sku'
import Spu from '@/components/pages/Spu'
import Specs from '@/components/pages/Specs'
import Options from '@/components/pages/Options'
import Channels from '@/components/pages/Channels'
import Brands from '@/components/pages/Brands'
import Pictures from '@/components/pages/Pictures'
import SpuAdd from '@/components/pages/SpuAdd'
import SpuEdit from '@/components/pages/SpuEdit'
import Order from '@/components/pages/Order'
import OrderDetail from '@/components/pages/OrderDetail'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'Login',
      component: Login
    },
    {
      path: '/home',
      name: 'Home',
      component: Home,
      children:[
          {
            path:'/home',
            name: 'Front',
            component: Front
          },
          {
            path:'/home/front',
            name: 'Front',
            component: Front
          },
          {
            path:'/home/user',
            name: 'User',
            component: User
          },
          {
            path:'/home/author',
            name: 'Authority',
            component: Authority
          },
          {
            path:'/home/group',
            name: 'Group',
            component: Group
          },
          {
            path:'/home/admin',
            name: 'Admin',
            component: Admin
          },
          {
            path:'/home/sku',
            name: 'Sku',
            component: Sku
          },
          {
            path:'/home/spu',
            name:'Spu',
            component:Spu
          },
          {
            path:'/home/specs',
            name:'Specs',
            component:Specs
          },
          {
            path:'/home/options',
            name:'Options',
            component:Options
          },
          {
            path:'/home/channels',
            name:'Channels',
            component:Channels
          },
          {
            path:'/home/brands',
            name:'Brands',
            component:Brands
          },
          {
            path:'/home/pictures',
            name:'Pictures',
            component:Pictures
          },
          {
            path:'/home/spuadd',
            name:'SpuAdd',
            component:SpuAdd
          },
          {
            path:'/home/spuedit',
            name:'SpuEdit',
            component:SpuEdit
          },
          {
            path:'/home/order',
            name:'Order',
            component:Order
          },
          {
            path:'/home/order_detail',
            name:'OrderDetail',
            component:OrderDetail
          }
      ]
    },
    {
      path: '*',
      name: 'NotFound',
      component: NotFound
    }
  ]
})
