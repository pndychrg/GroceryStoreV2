import { createRouter, createWebHistory } from "vue-router";
import HomeComponent from "./components/screens/home.vue";
import LoginComponent from "./components/screens/login.vue";
import RegisterComponent from "./components/screens/register.vue";

const routes = [
  {
    name: "home",
    path: "/",
    alias: "/home",
    component: HomeComponent,
    props: true,
  },
  {
    name: "login",
    path: "/login",
    component: LoginComponent,
  },
  {
    name: "register",
    path: "/register",
    component: RegisterComponent,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
