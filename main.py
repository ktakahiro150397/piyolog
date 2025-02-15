import asyncio
from datetime import datetime
import os

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import googleapiclient
import googleapiclient.discovery
from core.piyolog_parser.piyolog_parser_month import PiyoLogParserMonth
from logger_factory import LoggerFactory
from model.piyolog_day_record import PiyoLogDayRecord
import mysql.connector
from repository.piyolog_repository_base import PiyologRepositoryBase
from repository.piyolog_repository_mysql import PiyologRepositoryMySql
from googleapiclient.discovery import build
from itertools import groupby

logger = LoggerFactory.getLogger(__name__)

src_dir = "piyolog_data"
src_drive_dir = "piyolog_data_google_drive"

SCOPES = ["https://www.googleapis.com/auth/drive"]


def clear_dir(dir_path: str):
    for file in os.listdir(dir_path):
        if file.endswith(".txt"):
            os.remove(os.path.join(dir_path, file))


def get_google_drive_service() -> googleapiclient.discovery.Resource:
    logger.info("Create Google Drive service")

    # Credentialの取得または作成
    if os.path.exists("token.json"):
        logger.info("Use existing token.json")
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

        # If there are no (valid) credentials available, let the user log in.
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
    else:
        logger.info("Create new token.json")
        flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
        creds = flow.run_local_server()

    # Save the credentials for the next run
    with open("token.json", "w") as token:
        token.write(creds.to_json())

    service = build("drive", "v3", credentials=creds)

    logger.info("Google Drive service is created")
    return service


def get_google_drive_file(
    service: googleapiclient.discovery.Resource, filename: str, file_id: str
):
    request = service.files().get_media(fileId=file_id)
    fh = open(f"{src_drive_dir}/{filename}", "wb")
    downloader = googleapiclient.http.MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
    fh.close()
    logger.info(f"Download file: {filename}")


def delete_google_drive_file(service: googleapiclient.discovery.Resource, file_id: str):
    service.files().delete(
        fileId=file_id,
    ).execute()
    logger.debug(f"Delete file: {file_id}")


drive_service = get_google_drive_service()


async def main():
    previous_process_time = None
    while True:
        if (
            not previous_process_time is None
            and (datetime.now() - previous_process_time).seconds < 60
        ):
            logger.debug("Wait for 10 seconds...")
            await asyncio.sleep(10)
            continue

        previous_process_time = datetime.now()
        logger.info("Starting retrieve process...")
        await retrieve_data()
        logger.info("Retrieve process complete")


async def retrieve_data():
    try:
        file_list = []

        clear_dir(src_drive_dir)

        # マイドライブ > ぴよログ 以下のファイル一覧を取得
        results = (
            drive_service.files()
            .list(
                includeItemsFromAllDrives=True,
                supportsAllDrives=True,
                q="'1-3jwmeBYEzZpKqWXhDO3ziMq3H2aLQYO' in parents "
                "and trashed = false",
                orderBy="createdTime desc",
                fields="files(id, name, createdTime)",
                pageToken=None,
            )
            .execute()
        )

        files = results["files"]
        files.sort(key=lambda x: x["name"])

        logger.info(f"Google Drive file count: {len(files)}")

        # ファイル名ごとに、最も更新日付の新しいものを取得
        grouped_by_filename = {
            key: list(group) for key, group in groupby(files, key=lambda x: x["name"])
        }

        # キーごとに作成日時でソート
        for key in grouped_by_filename.keys():
            grouped_by_filename[key].sort(key=lambda x: x["createdTime"], reverse=True)

        # ドライブからファイルをダウンロード
        for key in grouped_by_filename.keys():
            file = grouped_by_filename[key][0]
            get_google_drive_file(drive_service, file["name"], file["id"])
            file_list.append(f"{src_drive_dir}/{file['name']}")

        # for dirpath, dirnames, filenames in os.walk(src_dir):
        #     for filename in filenames:
        #         # フルパスで取得する場合：
        #         file_path = os.path.join(dirpath, filename)
        #         file_list.append(file_path)

        if len(file_list) == 0:
            logger.info("No files to parse")
            return

        parser = PiyoLogParserMonth()

        month_data_list: list[PiyoLogDayRecord] = []
        for file in file_list:
            logger.info(f"Parsing file: {file}")

            with open(file, "r") as f:
                content = f.read()
                month_data = parser.parse_str(content)
                month_data_list.append(month_data)

        logger.info("Parse completed")

        # MySQLに接続
        conn = mysql.connector.connect(
            host="db", database="piyolog", user="docker", password="docker"
        )
        conn.autocommit = False

        if conn.is_connected():
            logger.debug("Connected to MySQL database")

            repo: PiyologRepositoryBase = PiyologRepositoryMySql(conn)

            for month_data in month_data_list:
                for day_data in month_data:
                    repo.delete_insert_piyolog(day_data)

            # データ登録後、一時ファイルを削除
            clear_dir(src_drive_dir)

            # Google Driveからファイルを削除
            for key in grouped_by_filename.keys():
                for file in grouped_by_filename[key]:
                    logger.info(f"Delete file: {file['name']} / {file['id']}")
                    delete_google_drive_file(drive_service, file["id"])

        else:
            logger.error("Failed to connect MySQL database")

        conn.close()
        logger.info("MySQL connection is closed")
    except Exception as e:
        logger.error(e, exc_info=True)
    finally:
        logger.info("Process is finished")


if __name__ == "__main__":
    asyncio.run(main())
