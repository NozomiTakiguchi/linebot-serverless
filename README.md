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
    * PackageType = Image にして、 Layer を利用すると同じようにコケるため、現時点では sam build -> local invoke は wsl 上で行う (devcontainer へのファイルマウント？の仕方が分からない)
    * Dockerfile で Layer で使用するディレクトリを PYTHONPATH に追加し、開発時にも参照できるようにする
    * /workspaces/linebot-serverless/lambda で `sam build --manifest ~/requirements.freeze.txt`
    * ホストの wsl 上で /workspaces/linebot-serverless/lambda で  `sam local invoke --env-vars ~/workspace/linebot-serverless/.env.json`
* `sam local start-lambda --container-host host.docker.internal` で localhost:3001 にエンドポイントが立つ
    * 現時点で CHANNEL_ACCESS_TOKEN 周りが keyerror になる
    * settings.py の読み方を工夫する必要がある
* terminal をもう一つ開いて、 `aws lambda invoke --function-name SomeFunctionName --endpoint http://localhost:3001/ output.txt`

## linebot からのリクエスト
* sam build までは↑と同じ
* ホストの wsl 上で /workspace/linebot-serverless/lambda で `sam local start-api --env-vars ~/workspace/linebot-serverless/.env.json`
* ngrok で `ngrok http 3000`
* line messaging api の webhookurl に `${生成された url}/${func: 今はテンプレートのままの hello}` を設定
    * build した後の最初のリクエスト受信で building image に時間がかかり token が expiring してしまう。仕方ない？
    * chromedriver executable may have wrong permissions となり 502 が返ってくる
        * .aws-sam/ に格納される chromedriver の権限を 755 にする
        * ただし、unexpectedly exit で怒られる
            * 多分ローカルの chrome とのバージョン齟齬とかだと思うので、やっぱり devcontainer 上で start api したい... (ファイルマウントの仕方が分からない)
