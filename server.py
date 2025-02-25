from fastapi import FastAPI

import json

from fastapi.responses import FileResponse
from logger_factory import LoggerFactory

logger = LoggerFactory.getLogger(__name__)

with open("server_settings.json") as f:
    settings = json.load(f)

logger.info("url: %s",settings["url"])
logger.info("width: %s",settings["width"])
logger.info("height: %s",settings["height"])

app = FastAPI()

@app.get("/")
async def read_root():
    return {"Hello","World"}

@app.get("/latest_pic")
async def latest_pic():
    """最新のURLの画像を取得して返します。"""

    return FileResponse(f"{settings["tempfilename"]}")

# uvicorn server:app --reload