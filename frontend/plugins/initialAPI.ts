import Vue from 'vue'

declare module 'vue/types/vue' {
  interface Vue {
    $initialAPI(that: any, apiName: string): void
  }
}

Vue.prototype.$initialAPI = async (that: any, apiName: string) => {
  that.plotly = require('plotly.js-dist')
  if (apiName === 'gpio') {
    that.graphDiv = document.getElementById('gpio-graph')
  } else if (apiName === 'daikin') {
    that.graphDiv = document.getElementById('daikin-graph')
  }

  const params = {} as any
  if (that.$route.query.limit) {
    params.limit = that.$route.query.limit
  }

  await that.$axios
    .get(that.apiUri, {
      params,
    })
    .then((res: any) => {
      that.apiData = res.data
    })
    .catch((err: any) => {
      console.error('API ERROR: ', err)
    })

  that.graphData.forEach((value: any) => {
    value.x = that.apiData.timestamp
    // @ts-ignore
    value.y = that.apiData[value.apiKey]
  })

  that.graphLayout.xaxis.autorange = true

  that.plotly.newPlot(that.graphDiv, that.graphData, that.graphLayout)
}
