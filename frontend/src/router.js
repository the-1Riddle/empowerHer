// router.js
import { createRouter, createWebHistory } from 'vue-router';
import Signup from './components/Signup.vue';
import Login from './components/Login.vue';
import Home from './components/Home.vue';
import Posts from './components/Posts.vue';
import Postpage from './components/Postpage.vue';

const routes = [
  { path: '/signup', name: 'signup', component: Signup },
  { path: '/login', name: 'login', component: Login },
  { path: '/', name: 'home', component: Home },
  { path: '/posts', name: 'posts', component: Posts },
  { path: '/postpage/:id', name: 'postpage', component: Postpage },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
