## usage
* ngrok で 多分 Endpoins > start Tunnel を押す
* ngrok.cmd を実行
* ngrok http ${port} を実行
* 表示される https パスを Line の MessagingAPI WebHookURL にペーストする
* devcontainer で開く
* linebot_agent.py を実行
* line で適当に文字入力
    * 複数の lambda ハンドラを作って、 api gateway で振り分ける感じのほうがよさそう
* ちゃんとポートが開くまでまたないとメッセージが届かない
* リッチメニューも CICD できるようにしたい

## リポジトリの設定
* branch name pattern = master に対して owner 以外の直 push を制限 (default)
* Require a pull request before merging を有効化
* GithubActions にて secrets を使用する場合は on push : master 時だけにする
* Repository secrets を利用
* collaborator は未設定

## Github Actions の設定
* jq コマンドの実行準備
    * インストーラ (jq-xxx.exe) をインストール、 jq.exe に rename して C:\\Program Files\Git\usr\bin に配置
* ssh keygen して、.pub を iam にアップロード
* github の secret に iam で確認できる .pub の ID と sec key を設定
* Codecommit リポジトリを作成 (後々 CDK でパイプライン作成したい)
* .github/workflows/mirroring.yml 作成