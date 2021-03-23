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
        temp: [],
        humi: [],
        press: [],
        co2: [],
        tvoc: [],
        ethanol: [],
        h2: [],
        timestamp: [],
      },

      weatherGraphData: [
        {
          name: 'Temp',
          type: 'scatter',
          x: [],
          y: [],
          apiKey: 'temp',
        },
        {
          name: 'Hum',
          type: 'scatter',
          yaxis: 'y2',
          x: [],
          y: [],
          apiKey: 'humi',
        },
        {
          name: 'Press',
          type: 'scatter',
          yaxis: 'y3',
          x: [],
          y: [],
          apiKey: 'press',
        },
        {
          name: 'CO2',
          type: 'scatter',
          yaxis: 'y4',
          x: [],
          y: [],
          hoverinfo: 'none',
          apiKey: 'co2',
        },

        {
          name: 'TVOC',
          type: 'bar',
          yaxis: 'y5',
          x: [],
          y: [],
          hoverinfo: 'none',
          marker: {
            color: 'rgb(158,225,177)',
            opacity: 0.5,
          },
          apiKey: 'tvoc',
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
          overlaying: 'y',
          fixedrange: true,
        },
        yaxis4: {
          visible: false,
          overlaying: 'y',
          fixedrange: true,
          range: [400, 3000],
        },
        yaxis5: {
          visible: false,
          overlaying: 'y',
          fixedrange: true,
          rangemode: 'nonnegative',
        },
      },
    }
  },
  computed: {
    latestData(): {} {
      return {
        temp: this.gpioAPIData.temp.slice(-1)[0],
        humi: this.gpioAPIData.humi.slice(-1)[0],
        press: this.gpioAPIData.press.slice(-1)[0],
        co2: this.gpioAPIData.co2.slice(-1)[0],
        tvoc: this.gpioAPIData.tvoc.slice(-1)[0],
        ethanol: this.gpioAPIData.ethanol.slice(-1)[0],
        h2: this.gpioAPIData.h2.slice(-1)[0],
        timestamp: this.gpioAPIData.timestamp.slice(-1)[0],
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

    this.weatherGraphData.forEach((value) => {
      value.x = this.gpioAPIData.timestamp
      // @ts-ignore
      value.y = this.gpioAPIData[value.apiKey]
    })

    this.plotly.newPlot(
      gpioGraphDiv,
      this.weatherGraphData,
      this.daikinGraphLayout
    )

    //  todo:追加でaxiosでminuteから4700個取得し、グラフを非同期に更新
    //  todo:hourのグラフを描画できるボタン用意、limitなしで全データ
    //  todo:ヘッダーの不要なボタン削除
    //  todo:コンパイルして、ラズパイのコンテナでSSRで動くか確認

    //  todo:光センサー追加する？
  },
})
</script>
