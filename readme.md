# Piyolog データ取得・可視化プログラム

## 説明

![ダッシュボードのサンプル画像](/docs/dashboard.jpg)

ぴよログからエクスポートしたデータを定期的に収集し、Grafanaで可視化できるプログラム(コンテナ群)です。

概要については以下の記事も合わせてご参照ください。

[ぴよログデータをGrafanaで可視化しよう！](www.google.com)

## プログラムの実行

### 前提条件

- Docker
- Docker Compose
- (Googleドライブ利用の場合)OAuth認証キー

### セットアップ

#### 1. **初期認証情報の作成:**

実行環境にブラウザが無い場合はGoogleの認証ができません。

そのため、`oauth.py`を実行して、初期認証情報を生成します。

Google Cloud Consoleで権限を付与したOauth2クライアントキーを`credential.json`にリネームし、`oauth.py`と同じディレクトリに配置してください。

ブラウザでの認証完了後に`token.json`が作成されます。

#### 2.  **環境変数の設定:**

以下の環境変数を設定します。

`.envsample.env`ファイルをコピーして`.env`ファイルを作成してください。

`GOOGLE_DRIVE_DIR_ID`は使用するGoogleドライブフォルダのIDを指定します。

**取得処理でフォルダ内のデータは削除されるので気を付けてください。**

同じく配置している`docker-compose.yaml`を使う場合はDB設定の変更の必要はありません。

|変数名|内容|
|--|--|
|`EXECUTION_INTERVAL`|データ取得間隔(秒)|
|`DIRECTORY_PATH`|データ取得時のワークディレクトリ|
|`GOOGLE_DRIVE_DIR_ID`|データを取得するGoogle DriveのディレクトリID|
|`PIYOLOG_DATA_DB_HOST`|データ保存先DBホスト|
|`PIYOLOG_DATA_DB_DATABASE`|データ保存先DBデータベース名|
|`PIYOLOG_DATA_DB_USER`|データ保存先DBユーザー|
|`PIYOLOG_DATA_DB_PASSWORD`|データ保存先DBパスワード|

#### 3.  **Docker Composeで実行:**

`docker compose up`を実行して、コンテナを起動します。

 - 定期的にデータ収集を行うPythonスクリプトが実行されます。
 - データを保存するMySQLが起動します。
 - `http://localhost:9000`でGrafanaダッシュボードにアクセスできます。

### コンテナの概要

####  **retriever:**

`main.py`を実行し、`EXECUTION_INTERVAL`秒ごとにデータ取得処理を行います。

Googleドライブからぴよログのエクスポートデータを取得し、パース後にDBへインサートしています。

パースロジックは`core/piyolog_parser`ディレクトリにあります。

####  **db:**

取得したデータを保存するためのMySQLインスタンスです。

データベーススキーマは`docker/db/sql/1_ddl.sql`で定義されています。(初回起動時に実行してテーブルを作成)

####  **grafana:**

データを可視化するためのGrafanaダッシュボードです。

`http://localhost:9000`でホストされます。

## 作成者について

[https://x.com/yanelmo3356?s=21&t=Xzg8KkeyECoX59vLhaeTIQ](https://x.com/yanelmo3356?s=21&t=Xzg8KkeyECoX59vLhaeTIQ)

## ライセンス

This project is licensed under the MIT License, see the LICENSE file for details.
