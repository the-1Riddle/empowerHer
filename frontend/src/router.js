// router.js
import { createRouter, createWebHistory } from 'vue-router';
import Signup from './components/Signup.vue';
import Login from './components/Login.vue';
import Home from './components/Home.vue';
import Posts from './components/Posts.vue';
import Wellness from './components/Wellness.vue';
import SexualAwareness from './components/SexualAwareness.vue';
import GenderViolence from './components/GenderViolence.vue';
import Postpage from './components/Postpage.vue';
import PrivacyPolicy from './components/PrivacyPolicy.vue';
import Account from './components/Account.vue';

const routes = [
  { path: '/signup', name: 'signup', component: Signup },
  { path: '/login', name: 'login', component: Login },
  { path: '/', name: 'home', component: Home },
  { path: '/posts', name: 'posts', component: Posts },
  { path: '/postpage/:id', name: 'postpage', component: Postpage },
  { path: '/sexual-awareness', name: 'sexual-awareness', component: SexualAwareness },
  { path: '/gender-violence', name: 'gender-violence', component: GenderViolence },
  { path: '/privacy-policy', name: 'privacy-policy', component: PrivacyPolicy },
  { path: '/wellness', name: 'wellness', component: Wellness },
  { path: '/account', name: 'account', component: Account },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
