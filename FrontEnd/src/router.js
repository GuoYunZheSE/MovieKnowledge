import Vue from 'vue';
import Router from 'vue-router';
import Home from './views/Home.vue';

Vue.use(Router);

export default new Router({
  routes: [
    {
      path: '/',
      name: 'home',
      component: Home,
    },
    {
      path: '/actor',
      name: 'Actor',
      component: () => import('./views/QueryActor'),
    },
    {
      path: '/movie',
      name: 'Movie',
      component: () => import('./views/QueryMovie'),
    },
  ],
});
