import { createApp } from "vue";
import App from "./App.vue";
import "bootstrap";
import "bootstrap/dist/css/bootstrap.min.css";
import router from "./services/router";
import { createPinia } from "pinia";
import "./services/axios";
import Toast from "vue-toastification";
// Import the CSS or use your own!
import "vue-toastification/dist/index.css";
import { userStateStore } from "./services/stateManager";

const pinia = createPinia();
const app = createApp(App);
app.use(router);
app.use(Toast);
app.use(pinia);

userStateStore().checkTokenOnAppStart();
app.mount("#app");

import "bootstrap/dist/js/bootstrap.js";
