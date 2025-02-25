from fastapi import FastAPI

import json

from fastapi.responses import FileResponse
from core.server.get_latest_pic import GetLatestPic
from logger_factory import LoggerFactory

logger = LoggerFactory.getLogger(__name__)

with open("server_settings.json") as f:
    settings = json.load(f)

# Kindle PaperWhite 10 gen
# 1072 × 1448
# → 1072 x 1300 くらい？

tempfilename = settings["tempfilename"]
url = settings["url"]
width = settings["width"]
height = settings["height"]

logger.info("tempfilename: %s",tempfilename)
logger.info("url: %s",url)
logger.info("width: %s",width)
logger.info("height: %s",height)

pic_getter = GetLatestPic(tempfilename)

app = FastAPI()

@app.get("/")
async def read_root():
    return {"Hello","World"}

@app.get("/latest_pic")
async def latest_pic():
    """最新のURLの画像を取得して返します。"""
    path = await pic_getter.get_latest_pic_from_url_async(url,width,height)
    return FileResponse(str(path))

@app.get("/latest_pic2")
def latest_pic2():
    path = pic_getter.get_latest_pic_from_url(url,width,height)
    return FileResponse(str(path))

@app.get("/latest_pic_selenium")
def latest_pic_selenium():
    path = pic_getter.get_latest_pic_from_url_selenium(url,width,height)
    return FileResponse(str(path))



# uvicorn server:app --reload