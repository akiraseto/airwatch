<template>
  <header>
    <b-navbar toggleable="lg" type="dark" variant="dark">
      <b-navbar-brand href="#">{{ title }}</b-navbar-brand>
    </b-navbar>
  </header>
</template>

<script lang="ts">
import Vue from 'vue'

export default Vue.extend({
  data() {
    return {
      title: 'AirWatch',
    }
  },

  methods: {},
})
</script>

<style scoped>
header {
  width: 100%;
  position: fixed;
  top: 0;
  left: 0;
  z-index: 100;
  background-color: #89b9c1;

  box-shadow: rgb(24 26 27 / 20%) 0 0.25rem 0.25rem,
    rgb(24 26 27 / 20%) 0 -1px 5px inset;
}
</style>
