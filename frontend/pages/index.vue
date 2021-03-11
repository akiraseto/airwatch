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
          name: 'Temp',
          type: 'scatter',
          x: [],
          y: [],
          apiKey: 'htemp',
        },
        {
          name: 'Hum',
          type: 'scatter',
          yaxis: 'y2',
          x: [],
          y: [],
          apiKey: 'hhum',
        },
        {
          name: 'Odor',
          type: 'bar',
          yaxis: 'y3',
          x: [],
          y: [],
          marker: {
            color: 'rgb(158,225,177)',
            opacity: 0.5,
          },
          apiKey: 'odor',
        },
        {
          name: 'PM25',
          type: 'bar',
          yaxis: 'y3',
          x: [],
          y: [],
          marker: {
            color: 'rgb(212,225,158)',
            opacity: 0.5,
          },
          apiKey: 'pm25',
        },
        {
          name: 'Dust',
          type: 'bar',
          yaxis: 'y3',
          // x: [],
          // y: [],
          marker: {
            color: 'rgb(225,185,158)',
            opacity: 0.5,
          },
          apiKey: 'dust',
        },
      ],

      daikinGraphLayout: {
        margin: { t: 50, b: 50 },
        paper_bgcolor: 'rgba(245,246,249,1)',
        plot_bgcolor: 'rgba(245,246,249,1)',
        showlegend: true,
        sizing: 'stretch',
        xaxis: {
          domain: [0, 0.99],
          type: 'date',
          // tickformat: '%m/%d %H:%M',
        },
        font: { size: 14 },
        yaxis: {
          title: 'Temp',
          titlefont: { color: '#1f77b4' },
          tickfont: { color: '#1f77b4' },
        },
        yaxis2: {
          title: 'Hum',
          titlefont: { color: '#ff7f0e' },
          tickfont: { color: '#ff7f0e' },
          anchor: 'free',
          overlaying: 'y',
          side: 'right',
          position: 0.99,
        },
        yaxis3: {
          visible: false,
          range: [0, 10],
          fixedrange: true,
          overlaying: 'y',
        },
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
    this.daikinGraphData.forEach((value) => {
      value.x = _this.daikinAPIData.timestamp
      value.y = _this.daikinAPIData[value.apiKey]
    })

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
