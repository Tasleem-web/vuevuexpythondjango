<template>
  <div id="app">
    <a-layout style="min-height: 100vh">
      <a-layout-header style="background: #001529; color: white; padding: 0">
        <div style="display: flex; align-items: center; color: white; padding: 0 24px">
          <h1 style="margin: 0; color: white">Vue.js + Vuex + Ant Design</h1>
        </div>
      </a-layout-header>
      <a-layout-content style="padding: 50px">
        <Home />
      </a-layout-content>
    </a-layout>
  </div>
</template>

<script>
import Home from './components/Home.vue'

export default {
  name: 'App',
  components: {
    Home
  }
}
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen',
    'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue',
    sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}
</style>
