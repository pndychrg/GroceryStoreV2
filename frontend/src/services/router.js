import { createRouter, createWebHistory } from "vue-router";
import HomeComponent from "../components/screens/home.vue";
import LoginComponent from "../components/screens/login.vue";
import RegisterComponent from "../components/screens/register.vue";
import { ROLES } from "./roles";
import { userStateStore } from "./stateManager";
import SectionsPage from "../components/screens/sections.vue";
import UserRatingPage from "../components/screens/user/user_rating.vue";
import AccessDenied from "../components/screens/accessDenied.vue";
import NotApproved from "../components/screens/admin/storeManager_notApproved.vue";
import ApproveManager from "../components/screens/admin/approve_manager.vue";
import ProductPage from "../components/screens/storemanager/products.vue";
import Dashboard from "../components/screens/dashboard.vue";
import CouponPage from "../components/screens/storemanager/coupons.vue";
const routes = [
  {
    name: "home",
    path: "/",
    alias: "/home",
    component: HomeComponent,
    meta: {
      requireAuth: true,
      roles: [ROLES.ADMIN, ROLES.STORE_MANAGER, ROLES.USER],
    },
  },
  {
    name: "sectionsPage",
    path: "/sections",
    alias: "/sections",
    component: SectionsPage,
    meta: { requireAuth: true, roles: [ROLES.ADMIN, ROLES.STORE_MANAGER] },
  },
  {
    name: "dashboard",
    path: "/dashboard",
    component: Dashboard,
    meta: { requireAuth: true },
  },
  {
    name: "CouponPage",
    path: "/coupons",
    component: CouponPage,
    meta: { requireAuth: true, roles: [ROLES.STORE_MANAGER] },
  },
  {
    name: "accessDenied",
    path: "/accessDenied",
    component: AccessDenied,
    meta: { requireAuth: true },
  },
  {
    name: "notApproved",
    path: "/notApproved",
    component: NotApproved,
    meta: { requireAuth: true, roles: [ROLES.NOT_APPROVED] },
  },
  {
    name: "approveManager",
    path: "/admin/approveManager",
    component: ApproveManager,
    meta: { requireAuth: true, roles: [ROLES.ADMIN] },
  },
  {
    name: "productsPage",
    path: "/products",
    component: ProductPage,
    meta: {
      requireAuth: true,
      roles: [ROLES.STORE_MANAGER],
    },
  },
  {
    name: "ratings",
    path: "/ratings",
    component: UserRatingPage,
    meta: {
      requireAuth: true,
      roles: [ROLES.USER],
    },
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
        next({ path: "/", replace: true });
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
  } else if (to.meta.roles && !to.meta.roles.includes(store.user.role)) {
    next("/accessDenied");
  } else {
    next();
  }
});

export default router;
