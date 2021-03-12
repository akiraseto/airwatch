module.exports = {
  root: true,
  env: {
    browser: true,
    node: true,
  },
  extends: [
    '@nuxtjs/eslint-config-typescript',
    'prettier',
    'prettier/vue',
    'plugin:prettier/recommended',
    'plugin:nuxt/recommended',
  ],
  plugins: ['prettier'],
  // add your custom rules here
  rules: {
    // console メソッドを注意
    'no-console': 0,
    // 連続スペースの許可
    'no-multi-spaces': 1,
    // 再代入がない限り const を強制
    'prefer-const': 2,
    // 連続した空行を注意
    'no-multiple-empty-lines': [1, { max: 3 }],
  },
}
