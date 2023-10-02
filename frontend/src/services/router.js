import { createRouter, createWebHistory } from "vue-router";
import HomeComponent from "../components/screens/home.vue";
import LoginComponent from "../components/screens/login.vue";
import RegisterComponent from "../components/screens/register.vue";
import { ROLES } from "./roles";
import { userStateStore } from "./stateManager";

const routes = [
  {
    name: "home",
    path: "/",
    alias: "/home",
    component: HomeComponent,
    meta: { requireAuth: true, roles: [ROLES.ADMIN, ROLES.ADMIN, ROLES.USER] },
  },
  {
    name: "login",
    path: "/login",
    component: LoginComponent,
    beforeEnter: (to, from, next) => {
      const store = userStateStore();
      if (store.isAuthenticated) {
        next({ path: "/", replace: true });
      } else {
        next();
      }
    },
  },
  {
    name: "register",
    path: "/register",
    component: RegisterComponent,
    beforeEnter: (to, from, next) => {
      const store = userStateStore();
      if (store.isAuthenticated) {
        next("/");
      } else {
        next();
      }
    },
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach((to, from, next) => {
  const store = userStateStore();
  if (to.meta.requireAuth && !store.isAuthenticated) {
    next("/login");
  } else {
    next();
  }
});

export default router;
