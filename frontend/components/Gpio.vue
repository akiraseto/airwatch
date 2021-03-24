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
      apiUri: '/api/v1/gpio',
      monthAmount: (60 * 24 * 31) / 10,
      firstSetTime: 4000,
      intervalTime: 1000 * 60 * 10,
      plotly: {} as any,

      graphDiv: null as any,
      apiData: {
        temp: [],
        humi: [],
        press: [],
        co2: [],
        tvoc: [],
        ethanol: [],
        h2: [],
        timestamp: [],
      },

      graphData: [
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

      graphLayout: {
        margin: { t: 50, b: 50 },
        paper_bgcolor: 'rgba(245,246,249,1)',
        plot_bgcolor: 'rgba(245,246,249,1)',
        showlegend: true,
        sizing: 'stretch',
        xaxis: {
          domain: [0, 0.99],
          type: 'date',
          autorange: false,
          range: [] as object,
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
        temp: this.apiData.temp.slice(-1)[0],
        humi: this.apiData.humi.slice(-1)[0],
        press: this.apiData.press.slice(-1)[0],
        co2: this.apiData.co2.slice(-1)[0],
        tvoc: this.apiData.tvoc.slice(-1)[0],
        ethanol: this.apiData.ethanol.slice(-1)[0],
        h2: this.apiData.h2.slice(-1)[0],
        timestamp: this.apiData.timestamp.slice(-1)[0],
      }
    },
  },
  async mounted() {
    this.plotly = require('plotly.js-dist')
    this.graphDiv = document.getElementById('gpio-graph')

    const params = {} as any
    if (this.$route.query.limit) {
      params.limit = this.$route.query.limit
    }

    await this.$axios
      .get(this.apiUri, {
        params,
      })
      .then((res) => {
        this.apiData = res.data
      })
      .catch((err) => {
        console.error('API ERROR: ', err)
      })

    this.graphData.forEach((value) => {
      value.x = this.apiData.timestamp
      // @ts-ignore
      value.y = this.apiData[value.apiKey]
    })

    this.graphLayout.xaxis.autorange = true

    this.plotly.newPlot(this.graphDiv, this.graphData, this.graphLayout)

    setTimeout(() => {
      this.repeatedAPI()
    }, this.firstSetTime)

    setInterval(() => {
      this.repeatedAPI()
    }, this.intervalTime)
  },
  methods: {
    repeatedAPI() {
      console.log('repeat GPIO API')

      this.$axios
        .get(this.apiUri, {
          params: {
            limit: this.monthAmount,
          },
        })
        .then((res) => {
          if (
            JSON.stringify(Object.entries(this.apiData).sort()) !==
            JSON.stringify(Object.entries(res.data).sort())
          ) {
            console.log('GPIO Data is changed')

            this.apiData = res.data

            this.graphData.forEach((value) => {
              value.x = this.apiData.timestamp
              // @ts-ignore
              value.y = this.apiData[value.apiKey]
            })

            this.graphLayout.xaxis.autorange = false
            this.graphLayout.xaxis.range = [
              this.$moment().add(-1, 'days').toDate(),
              this.$moment().toDate(),
            ]

            let co2Max = this.graphLayout.yaxis4.range[1]
            this.graphData.forEach(function (value: any) {
              if (value.apiKey === 'co2') {
                co2Max = value.y.reduce((a: number, b: number) => {
                  return Math.max(a, b)
                })
              }
            })
            this.graphLayout.yaxis4.range[1] = co2Max

            this.apiData = res.data
            this.plotly.update(this.graphDiv, this.graphData, this.graphLayout)
          }
        })
        .catch((err) => {
          console.error('API ERROR: ', err)
        })
    },
  },
})
</script>
