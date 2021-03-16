<template>
  <div class="container-wrapper container-fluid">
    <div class="row justify-content-center">
      <div class="col-11">
        <Daikin />
        <Gpio />
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import Vue from 'vue'

export default Vue.extend({
  data() {
    return {}
  },
})
</script>

<style>
.container-wrapper {
  padding-top: 60px;
}
</style>
