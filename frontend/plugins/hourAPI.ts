import Vue from 'vue'

declare module 'vue/types/vue' {
  interface Vue {
    $hourAPI(that: any, apiName: string): void
  }
}

Vue.prototype.$hourAPI = async (that: any, apiName: string) => {
  console.log('make Hour Graph')

  that.plotly = require('plotly.js-dist')
  let hourGraphDiv: HTMLElement | null = null
  if (apiName === 'gpio') {
    hourGraphDiv = document.getElementById('gpio-hour-graph')
  } else if (apiName === 'daikin') {
    hourGraphDiv = document.getElementById('daikin-hour-graph')
  }

  const params = {
    period: 'hour',
    limit: null as any,
  }
  if (that.$route.query.limit) {
    params.limit = that.$route.query.limit
  }

  let hourApiData = { ...that.apiData }
  await that.$axios
    .get(that.apiUri, {
      params,
    })
    .then((res: any) => {
      hourApiData = res.data
    })
    .catch((err: any) => {
      console.error('API ERROR: ', err)
    })

  const hourGraphData = that.graphData.map((value: any) => {
    value.x = hourApiData.timestamp
    // @ts-ignore
    value.y = hourApiData[value.apiKey]
    return value
  })

  const hourGraphLayout = { ...that.graphLayout }

  hourGraphLayout.xaxis.autorange = true

  that.plotly.newPlot(hourGraphDiv, hourGraphData, hourGraphLayout)
}
