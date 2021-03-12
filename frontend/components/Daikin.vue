<template>
  <div class="my-1">
    <h3>ダイキン</h3>

    <b-list-group horizontal="sm" class="mt-3">
      <b-list-group-item> Temp: {{ latestData['htemp'] }} </b-list-group-item>
      <b-list-group-item> Hum: {{ latestData['hhum'] }} </b-list-group-item>
      <b-list-group-item> Odor: {{ latestData['odor'] }} </b-list-group-item>
      <b-list-group-item> PM25: {{ latestData['pm25'] }} </b-list-group-item>
      <b-list-group-item> Dust: {{ latestData['dust'] }} </b-list-group-item>
    </b-list-group>
    <p class="small text-secondary">{{ latestData['timestamp'] }}</p>

    <div id="daikin-graph"></div>
    <!-- todo:グラフ範囲変更する？(分、時、日、週間)-->
  </div>
</template>

<script lang="ts">
import Vue from 'vue'

export default Vue.extend({
  data() {
    return {
      title: 'airwatch',
      plotly: {} as any,

      daikinAPIData: {
        htemp: [],
        hhum: [],
        pm25: [],
        dust: [],
        odor: [],
        timestamp: [],
      },

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
          hoverinfo: 'none',
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
          hoverinfo: 'none',
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
          x: [],
          y: [],
          hoverinfo: 'none',
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
      return {
        htemp: this.daikinAPIData.htemp.slice(-1)[0],
        hhum: this.daikinAPIData.hhum.slice(-1)[0],
        pm25: this.daikinAPIData.pm25.slice(-1)[0],
        dust: this.daikinAPIData.dust.slice(-1)[0],
        odor: this.daikinAPIData.odor.slice(-1)[0],
        timestamp: this.daikinAPIData.timestamp.slice(-1)[0],
      }
    },
  },
  async mounted() {
    setInterval(() => {
      console.log('time')
    }, 3000)

    this.plotly = require('plotly.js-dist')
    const daikinGraphDiv = document.getElementById('daikin-graph')

    await this.$axios
      .get('/api/v1/daikin')
      .then((res) => {
        this.daikinAPIData = res.data
      })
      .catch((err) => {
        console.error('API ERROR: ', err)
      })

    this.daikinGraphData.forEach((value) => {
      value.x = this.daikinAPIData.timestamp
      // @ts-ignore
      value.y = this.daikinAPIData[value.apiKey]
    })

    this.plotly.newPlot(
      daikinGraphDiv,
      this.daikinGraphData,
      this.daikinGraphLayout
    )
  },
})
</script>
