<template>
  <div id="app">
    <django-health/>
    <websocket/>
  </div>
</template>

<script>
import DjangoHealth from './components/DjangoHealth.vue'
import Websocket from './components/Websocket.vue'
export default {
  name: 'App',
  components: {
    DjangoHealth,
    Websocket
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
  margin-top: 60px;
}
</style>
