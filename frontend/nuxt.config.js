export default {
  ssr: false,
  server: {
    host: '0.0.0.0', // デフォルト: localhost
  },
  // Global page headers: https://go.nuxtjs.dev/config-head
  head: {
    title: 'airwatch',
    htmlAttrs: {
      lang: 'en',
    },
    meta: [
      { charset: 'utf-8' },
      { name: 'viewport', content: 'width=device-width, initial-scale=1' },
      { hid: 'description', name: 'description', content: '' },
    ],
    link: [{ rel: 'icon', type: 'image/x-icon', href: '/favicon.ico' }],
  },

  // Global CSS: https://go.nuxtjs.dev/config-css
  css: [],

  // Plugins to run before rendering page: https://go.nuxtjs.dev/config-plugins
  plugins: [
    { src: '~/plugins/repeatedAPI' },
    { src: '~/plugins/initialAPI' },
    { src: '~/plugins/hourAPI' },
  ],

  // Auto import components: https://go.nuxtjs.dev/config-components
  components: true,

  // Modules for dev and build (recommended): https://go.nuxtjs.dev/config-modules
  buildModules: [
    // https://go.nuxtjs.dev/typescript
    '@nuxt/typescript-build',
    '@nuxtjs/moment',
  ],

  // Modules: https://go.nuxtjs.dev/config-modules
  modules: [
    // https://go.nuxtjs.dev/bootstrap
    'bootstrap-vue/nuxt',
    // https://go.nuxtjs.dev/axios
    '@nuxtjs/axios',
    '@nuxtjs/proxy',
  ],

  // moment: {
  //   locales: ['ja'],
  // },
  // Axios module configuration: https://go.nuxtjs.dev/config-axios
  // axios: {
  //   proxy: true,
  // },
  // proxy: {
  //   '/api/': {
  //     // target: 'http://localhost:5000',
  //     pathRewrite: { '^/api/': '' },
  //   },
  // },

  // Build Configuration: https://go.nuxtjs.dev/config-build
  build: {
    babel: {
      babelrc: false,
      compact: false,
    },
  },
}
