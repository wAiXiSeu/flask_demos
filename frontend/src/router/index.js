import Vue from 'vue'
import Router from 'vue-router'
import HelloWorld from '@/components/HelloWorld'
import Dockers from "@/components/Dockers";
import Emr from "@/components/Emr";

Vue.use(Router);

export default new Router({
  routes: [
    {
      path: '/',
      name: 'HelloWorld',
      component: HelloWorld
    },
    {
      path: '/dockers',
      name: 'Dockers',
      component: Dockers
    },
    {
      path: '/emr',
      name: 'EMR',
      component: Emr
    }
  ]
})
