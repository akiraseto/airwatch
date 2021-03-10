<template>
  <header>
    <b-navbar toggleable="lg" type="dark" variant="dark">
      <b-navbar-brand href="#">{{ title }}</b-navbar-brand>

      <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>

      <b-collapse id="nav-collapse" is-nav>
        <b-navbar-nav>
          <b-nav-item href="#">Link</b-nav-item>
          <b-nav-item href="#" disabled>Disabled</b-nav-item>
        </b-navbar-nav>

        <!-- Right aligned nav items -->
        <b-navbar-nav class="ml-auto"></b-navbar-nav>
      </b-collapse>
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
