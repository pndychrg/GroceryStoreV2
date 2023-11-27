<template>
  <navbar />
  <div class="d-flex justify-content-center align-items-center">
    <div class="container-fluid w-100 ">
      <router-view style="margin-top: 60px;">
      </router-view>
    </div>
  </div>
</template>

<script>
import Navbar from './components/widgets/navbar.vue';
export default {
  name: 'App',
  components: {
    Navbar
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  height: 100%;
}

html,
#app,
body {
  height: 100%;
}

.container {
  height: 100%;
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
}

/* .RouterContainer {
  border-top-right-radius: 20%;
} */
</style>
