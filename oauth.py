import os
import json

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from logger_factory import LoggerFactory
from googleapiclient.discovery import build

logger = LoggerFactory.getLogger(__name__)

# コンテナ環境などのブラウザがない場合、事前に認証しておくためのヘルパースクリプトです。
def generate_token():
    # 1. token.jsonが存在する場合は削除
    if os.path.exists('token.json'):
        os.remove('token.json')
        logger.info("token.json deleted")

    # 2. スコープを設定
    SCOPES = ["https://www.googleapis.com/auth/drive"]

    # 3. Credentialの取得または作成
    logger.info("Create new token.json")
    # 3.1. credentials.jsonからフローを作成
    flow = InstalledAppFlow.from_client_secrets_file(
        "credentials.json", scopes=SCOPES
    )
    # 3.2. 認証フローを実行
    creds = flow.run_local_server()

    try:
        # 4. Drive APIを呼び出して認証情報を検証
        service = build("drive", "v3", credentials=creds)
        user_info = service.about().get(fields="user").execute()
        logger.info(f"認証情報の検証に成功しました。user_info: {user_info}")
    except Exception as e:
        logger.error(f"認証情報の検証に失敗しました: {e}", exc_info=True)
        return

    # 5. Credentialをtoken.jsonに保存
    with open("token.json", "w") as token:
        token.write(creds.to_json())

    logger.info("token.json generated successfully.")

if __name__ == "__main__":
    generate_token()
