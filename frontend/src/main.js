import { createApp } from "vue";
import App from "./App.vue";
import "bootstrap";
import "bootstrap/dist/css/bootstrap.min.css";
import "bootstrap/dist/js/bootstrap.min.js";
import router from "./services/router";
import { createPinia } from "pinia";
import "./services/axios";
import Toast from "vue-toastification";
// Import the CSS or use your own!
import "vue-toastification/dist/index.css";
import { userStateStore } from "./services/stateManager";
import axios from "./services/axios";
/* import the fontawesome core */
/* import font awesome icon component */
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import "font-awesome-animation/css/font-awesome-animation.min.css";
// eslint-disable-next-line no-unused-vars
import { iconLib } from "./static/js/icons";
// import { CartStateStore } from "./services/cartStateManager";
const pinia = createPinia();
const app = createApp(App);
app.use(router);
app.use(Toast);
app.use(pinia);
const store = userStateStore();
axios.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response && error.response.status === 401) {
      store.logoutUser();
      return Promise.reject(error);
    }
    return Promise.reject(error);
  }
);
// pinia.use(CartStateStore);
app.component("font-awesome-icon", FontAwesomeIcon);
userStateStore().checkTokenOnAppStart();
app.mount("#app");

// import "bootstrap/dist/js/bootstrap.js";
