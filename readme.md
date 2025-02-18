# Piyolog データ取得・可視化プログラム

## 説明

ぴよログからエクスポートしたデータを定期的に収集し、Grafanaで可視化できるコンテナ群です。

概要については以下も合わせてご参照ください。

TODO : Zenn URLを記載

## プログラムの実行

### 前提条件

*   Docker
*   Docker Compose

### セットアップ

1.  **初期認証情報の作成:**

    実行環境にブラウザが無い場合はGoogleの認証ができません。
    そのため、`oauth.py`を実行して、初期認証情報を生成します。
    
    Google Cloud Consoleで権限を付与したOauth2クライアントキーを`credential.json`にリネームし、`oauth.py`と同じディレクトリに配置してください。

    実行し、ブラウザでの認証完了後に`token.json`が作成されます。

2.  **環境変数の設定:**

    以下の環境変数を設定します。
    `.envsample.env`ファイルをコピーして`.env`ファイルを作成してください。
    
    `GOOGLE_DRIVE_DIR_ID`は使用するGoogleドライブフォルダのIDを指定します。
    **取得処理でフォルダ内のデータは削除されるので気を付けてください。**

    同じく配置している`docker-compose.yaml`を使う場合はDB設定の変更の必要はありません。

    *   `EXECUTION_INTERVAL`: データ取得間隔(秒)。
    *   `DIRECTORY_PATH`: データ取得時のワークディレクトリ。
    *   `GOOGLE_DRIVE_DIR_ID`: データを取得するGoogle DriveのディレクトリID。
    *   `PIYOLOG_DATA_DB_HOST`: データ保存先DBホスト。
    *   `PIYOLOG_DATA_DB_DATABASE`: データ保存先DBデータベース名。
    *   `PIYOLOG_DATA_DB_USER`: データ保存先DBユーザー。
    *   `PIYOLOG_DATA_DB_PASSWORD`: データ保存先DBパスワード。

3.  **Docker Composeで実行:**

    `docker compose up`を実行して、コンテナを起動します。

### コンテナの概要

*   **retriever:**

    このコンテナは`main.py`を実行します。これはメインのアプリケーションロジックです。指定されたソース（例：Googleドライブ）からデータを取得し、解析してMySQLデータベースに挿入します。データ解析ロジックは`core/piyolog_parser`ディレクトリにあります。データベースとのやり取りは、`repository`ディレクトリのクラスによって処理されます。

*   **db:**

    このコンテナは、取得したデータを保存するためのMySQLインスタンスを提供します。データベーススキーマは`docker/db/sql/1_ddl.sql`で定義されています。MySQLの設定は`docker/db/my.cnf`にあります。

*   **grafana:**

    このコンテナは、データを可視化するためのGrafanaダッシュボードをホストします。ダッシュボードの設定は`grafana_dashbord.json`にあります。このダッシュボードをGrafanaインスタンスにインポートして、データを可視化できます。
