<template>
  <div id="app">
      <Map/>

    <!-- <django-health/>
    <websocket/>
    <startup/>
    <Tweet id="692527862369357824"></Tweet> -->
  </div>
</template>

<script>
import Map from './components/Map.vue'
export default {
  name: 'App',
  components: {
    Map,

  }
}
</script>

<style>
/* #app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;

} */

html,body,#app,#map {
  height: 100%;
  margin: 0;
}
.wrapper {
  width: 100%;
  margin: 0;

}

.menu {
  height: 100px;
  margin: 0;
}
@import url("~leaflet/dist/leaflet.css");
</style>
