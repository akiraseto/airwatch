<template>
  <div class="container-wrapper container-fluid">
    <div class="row justify-content-center">
      <div class="col-11">
        <div class="my-1">
          <h3>ダイキン</h3>
          <b-list-group horizontal="sm" class="mt-3">
            <b-list-group-item>
              Temp: {{ latestList['htemp'] }}
            </b-list-group-item>
            <b-list-group-item>
              Hum: {{ latestList['hhum'] }}
            </b-list-group-item>
            <b-list-group-item>
              Odor: {{ latestList['odor'] }}
            </b-list-group-item>
            <b-list-group-item>
              PM25: {{ latestList['pm25'] }}
            </b-list-group-item>
            <b-list-group-item>
              Dust: {{ latestList['dust'] }}
            </b-list-group-item>
          </b-list-group>
          <p class="small text-secondary">{{ latestList['timestamp'] }}</p>

          <pre>
            グラフ5分(12時間分？)
            グラフ変更パネル(範囲、時、日、週間)
          </pre>
        </div>
        <div class="my-1">
          <h3>ラズパイセンサー</h3>
          <pre>
            ラズパイのグラフ5分
          </pre>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import Vue from 'vue'

export default Vue.extend({
  async asyncData({ $axios }) {
    const daikinData = await $axios.$get('/api/v1/daikin')
    return { daikinData }
  },
  data() {
    return {
      title: 'airwatch',
    }
  },
  computed: {
    latestList(): {} {
      return (this as any).daikinData.slice(-1)[0]
    },
  },

  methods: {},
})
</script>

<style>
.container-wrapper {
  padding-top: 60px;
}
</style>

<!--todo:daikinの最新データ表示-->
