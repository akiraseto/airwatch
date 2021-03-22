<template>
  <div class="my-3">
    <h3>{{ title }}</h3>

    <b-list-group horizontal="sm" class="mt-3">
      <b-list-group-item> Temp: {{ latestData['temp'] }}°C </b-list-group-item>
      <b-list-group-item> Hum: {{ latestData['humi'] }}% </b-list-group-item>
      <b-list-group-item>
        Press: {{ latestData['press'] }}hPa
      </b-list-group-item>
      <b-list-group-item> CO2: {{ latestData['co2'] }}ppm </b-list-group-item>
      <b-list-group-item> TVOC: {{ latestData['tvoc'] }}ppb </b-list-group-item>
      <b-list-group-item>
        Ethanol: {{ latestData['ethanol'] }}ppm
      </b-list-group-item>
      <b-list-group-item> H2: {{ latestData['h2'] }}ppm </b-list-group-item>
    </b-list-group>
    <p class="small text-secondary">{{ latestData['timestamp'] }}</p>

    <div id="gpio-graph"></div>
  </div>
</template>

<script lang="ts">
import Vue from 'vue'

export default Vue.extend({
  data() {
    return {
      title: 'GPIOセンサー',
      plotly: {} as any,

      gpioAPIData: {
        bmp: {
          temp: [],
          timestamp: [],
          press: [],
        },
        dht: {
          humi: [],
          temp: [],
        },
        sgp: {
          co2: [],
          tvoc: [],
          ethanol: [],
          h2: [],
        },
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
        temp:
          (this.gpioAPIData.bmp.temp.slice(-1)[0] +
            this.gpioAPIData.dht.temp.slice(-1)[0]) /
          2,
        humi: this.gpioAPIData.dht.humi.slice(-1)[0],
        press: this.gpioAPIData.bmp.press.slice(-1)[0] / 100,
        co2: this.gpioAPIData.sgp.co2.slice(-1)[0],
        tvoc: this.gpioAPIData.sgp.tvoc.slice(-1)[0],
        ethanol: this.gpioAPIData.sgp.ethanol.slice(-1)[0],
        h2: this.gpioAPIData.sgp.h2.slice(-1)[0],
        timestamp: this.gpioAPIData.bmp.timestamp.slice(-1)[0],
      }
    },
  },
  async mounted() {
    this.plotly = require('plotly.js-dist')
    const gpioGraphDiv = document.getElementById('gpio-graph')

    await this.$axios
      .get('/api/v1/gpio')
      .then((res) => {
        this.gpioAPIData = res.data
      })
      .catch((err) => {
        console.error('API ERROR: ', err)
      })
    //
    // this.daikinGraphData.forEach((value) => {
    //   value.x = this.gpioAPIData.timestamp
    //   // @ts-ignore
    //   value.y = this.gpioAPIData[value.apiKey]
    // })
    //
    // this.plotly.newPlot(
    //   daikinGraphDiv,
    //   this.daikinGraphData,
    //   this.daikinGraphLayout
    // )
  },
})
</script>
