* ngrok で 多分 Endpoins > start Tunnel を押す
* downloads > ngrok xxx に配置されている ngrok.cmd? を実行
* ngrok http 9000 を実行
* 表示される https パスを Line の MessagingAPI のところに貼る
* devcontainer で開く
* export で CHANNEL_ACCESS_TOKEN と CHANNEL_SECRET と PORT を定義する
* linebot_agent.py を実行
* line で適当に文字入力
    * 複数の lambda ハンドラを作って、 api gateway で振り分ける感じのほうがよさそう
* ちゃんとポートが開くまでまたないとメッセージが届かない
* リッチメニューも CICD できるようにしたい