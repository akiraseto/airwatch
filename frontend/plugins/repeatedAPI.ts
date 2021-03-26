import Vue from 'vue'

declare module 'vue/types/vue' {
  interface Vue {
    $repeatedAPI(that: any, apiName: string): void
  }
}

Vue.prototype.$repeatedAPI = (that: any, apiName: string) => {
  console.log(`repeat ${apiName.toUpperCase()} API`)

  const apiUri = `http://${location.host}:5000/v1/${apiName}`
  that.$axios
    .get(apiUri, {
      params: {
        limit: that.monthAmount,
      },
    })
    .then((res: any) => {
      if (
        JSON.stringify(Object.entries(that.apiData).sort()) !==
        JSON.stringify(Object.entries(res.data).sort())
      ) {
        console.log(`${apiName.toUpperCase()} Data is changed`)

        that.apiData = res.data

        that.graphData.forEach((value: any) => {
          value.x = that.apiData.timestamp
          // @ts-ignore
          value.y = that.apiData[value.apiKey]
        })

        that.graphLayout.xaxis.autorange = false
        that.graphLayout.xaxis.range = [
          that.$moment().add(-1, 'days').toDate(),
          that.$moment().toDate(),
        ]

        if (apiName === 'gpio') {
          let co2Max = that.graphLayout.yaxis4.range[1]
          that.graphData.forEach(function (value: any) {
            if (value.apiKey === 'co2') {
              co2Max = value.y.reduce((a: number, b: number) => {
                return Math.max(a, b)
              })
            }
          })
          that.graphLayout.yaxis4.range[1] = co2Max
        }

        that.apiData = res.data
        that.plotly.update(that.graphDiv, that.graphData, that.graphLayout)
      }
    })
    .catch((err: any) => {
      console.error('API ERROR: ', err)
    })
}
