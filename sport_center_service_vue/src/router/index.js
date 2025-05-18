import { createRouter, createWebHistory } from 'vue-router'
import MainPage from '../pages/Main.vue'
import LoginPage from '../pages/Login.vue'
import RegistrationPage from "../pages/Registration.vue";

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/login',
      name: 'Login',
      component: LoginPage },

    { path: '/register',
      name: 'Registration',
      component: RegistrationPage },

    { path: '/',
      name: 'Main',
      component: MainPage,
      meta: { requiresAuth: true } },

  ],
})

router.beforeEach((to, from, next) => {
  const isAuthenticated = localStorage.getItem('authToken') !== null;

  if (to.meta.requiresAuth && !isAuthenticated) {
    next('/login');
  } else {
    next();
  }
});

export default router;
