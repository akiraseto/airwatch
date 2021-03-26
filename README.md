# airwatch
ダイキン空気清浄機
ラズパイセンサー

Nuxt.js
TypeScript
Docker
Plotly.js

## query
URLクエリ`?limit=30`をつけることでグラフの初期描画データ数を指定することができる。


## memo
Dockerのnodeコンテナでnuxt.js試用メモ。
- build及び、devは`JavaScript heap out of memory`によりエラーで不可
- 事前にnode_modules,`npm run build`して用意してもエラー。おそらく自らbuildしないと使えない？
- ラズパイのスワップメモリーを増強。Nodeのデフォルトメモリ上限の2GBに引き上げるが、heap out of memoryでエラー。

そのため、mode:staticでgenerateしてSPAサイトをnginxコンテナで構築する。


## フロントページのジェネレート
Nginxで描画するhtmlページをローカルのNuxt.jsでgenerateする。  
`npm run generate`  

