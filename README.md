## usage
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

## AWS SAM CLI の実行
* sam init / sam build 実行
    * sam init にて PackageType = Zip にすると、ホストでは正常に local invoke できるが devcontainer 上では no module named app によりコケる (原因は現時点で不明)
* `sam local start-lambda --container-host host.docker.internal` で localhost:3001 にエンドポイントが立つ
* terminal をもう一つ開いて、 `aws lambda invoke --function-name SomeFunctionName --endpoint http://localhost:3001/ output.txt`

## linebot からのリクエスト
* ngrok の利用