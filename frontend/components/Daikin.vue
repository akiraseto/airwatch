<template>
  <div class="my-3">
    <h3>{{ title }}</h3>

    <b-list-group horizontal="sm" class="mt-3">
      <b-list-group-item> Temp: {{ latestData['temp'] }}°C </b-list-group-item>
      <b-list-group-item> Hum: {{ latestData['hum'] }}% </b-list-group-item>
      <b-list-group-item> Odor: {{ latestData['odor'] }} </b-list-group-item>
      <b-list-group-item> PM25: {{ latestData['pm25'] }} </b-list-group-item>
      <b-list-group-item> Dust: {{ latestData['dust'] }} </b-list-group-item>
    </b-list-group>
    <p class="small text-secondary">{{ latestData['timestamp'] }}</p>

    <b-card no-body>
      <b-tabs pills card>
        <b-tab title="Minute" active>
          <div id="daikin-graph"></div>
        </b-tab>
        <b-tab title="Hour" @click="hourAPI">
          <div id="daikin-hour-graph"></div>
        </b-tab>
      </b-tabs>
    </b-card>
  </div>
</template>

<script lang="ts">
import Vue from 'vue'

export default Vue.extend({
  data() {
    return {
      title: 'ダイキン',
      apiUri: '/api/v1/daikin',
      monthAmount: (60 * 24 * 31) / 10,
      firstSetTime: 4000,
      intervalTime: 1000 * 60 * 10,
      plotly: {} as any,

      graphDiv: null as any,
      apiData: {
        htemp: [],
        hhum: [],
        pm25: [],
        dust: [],
        odor: [],
        timestamp: [],
      },

      graphData: [
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

      graphLayout: {
        margin: { t: 50, b: 50 },
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
        temp: this.apiData.htemp.slice(-1)[0],
        hum: this.apiData.hhum.slice(-1)[0],
        pm25: this.apiData.pm25.slice(-1)[0],
        dust: this.apiData.dust.slice(-1)[0],
        odor: this.apiData.odor.slice(-1)[0],
        timestamp: this.apiData.timestamp.slice(-1)[0],
      }
    },
  },
  mounted() {
    this.$initialAPI(this, 'daikin')

    setTimeout(() => {
      this.$repeatedAPI(this, 'daikin')
    }, this.firstSetTime)

    setInterval(() => {
      this.$repeatedAPI(this, 'daikin')
    }, this.intervalTime)
  },
  methods: {
    hourAPI() {
      this.$hourAPI(this, 'daikin')
    },
  },
  //  todo:コンパイルして、ラズパイのコンテナでSSRで動くか確認

  //  todo:光センサー追加？
})
</script>
