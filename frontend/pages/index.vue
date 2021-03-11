<template>
  <div class="container-wrapper container-fluid">
    <div class="row justify-content-center">
      <div class="col-11">
        <div class="my-1">
          <h3>ダイキン</h3>

          <b-list-group horizontal="sm" class="mt-3">
            <b-list-group-item>
              Temp: {{ latestData['htemp'] }}
            </b-list-group-item>
            <b-list-group-item>
              Hum: {{ latestData['hhum'] }}
            </b-list-group-item>
            <b-list-group-item>
              Odor: {{ latestData['odor'] }}
            </b-list-group-item>
            <b-list-group-item>
              PM25: {{ latestData['pm25'] }}
            </b-list-group-item>
            <b-list-group-item>
              Dust: {{ latestData['dust'] }}
            </b-list-group-item>
          </b-list-group>
          <p class="small text-secondary">{{ latestData['timestamp'] }}</p>

          <div id="daikin-graph"></div>

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
    const daikinAPIData = await $axios.$get('/api/v1/daikin')
    return { daikinAPIData }
  },
  data() {
    return {
      title: 'airwatch',
      plotly: {} as any,

      daikinGraphData: [
        {
          x: [
            '2021-10-04 22:23:00',
            '2021-11-04 22:23:00',
            '2021-12-04 22:23:00',
          ],
          y: [1, 2, 3],
          type: 'scatter',
        },
      ],

      daikinGraphLayout: {
        paper_bgcolor: 'rgba(245,246,249,1)',
        plot_bgcolor: 'rgba(245,246,249,1)',
        showlegend: false,
        sizing: 'stretch',
        font: { size: 14 },
        xaxis: {},
        yaxis: {
          // range: [0, 10],
        },
        bargap: 0.05,
      },
    }
  },
  computed: {
    latestData(): {} {
      const _this = this as any
      return {
        htemp: _this.daikinAPIData.htemp.slice(-1)[0],
        hhum: _this.daikinAPIData.hhum.slice(-1)[0],
        pm25: _this.daikinAPIData.pm25.slice(-1)[0],
        dust: _this.daikinAPIData.dust.slice(-1)[0],
        odor: _this.daikinAPIData.odor.slice(-1)[0],
        timestamp: _this.daikinAPIData.timestamp.slice(-1)[0],
      }
    },
  },
  mounted() {
    this.plotly = require('plotly.js-dist')
    const daikinGraphDiv = document.getElementById('daikin-graph')

    const _this = this as any
    // _this.daikinAPIData.timestamp = _this.daikinAPIData.timestamp.map(function (
    //   v: string
    // ) {
    //   return _this.$moment(v).format('YYYY-MM-DD HH:mm:ss')
    // })

    this.daikinGraphData[0].x = _this.daikinAPIData.timestamp
    this.daikinGraphData[0].y = _this.daikinAPIData.htemp

    this.plotly.newPlot(
      daikinGraphDiv,
      this.daikinGraphData,
      this.daikinGraphLayout
    )
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
