from fastapi import FastAPI

import json

from fastapi.responses import FileResponse
from get_latest_pic import GetLatestPic

with open("server_settings.json") as f:
    settings = json.load(f)

# Kindle PaperWhite 10 gen
# 1072 × 1448
# → 1072 x 1300 くらい？

tempfilename = settings["tempfilename"]
url = settings["url"]

# logger.info("tempfilename: %s",tempfilename)
# logger.info("url: %s",url)

pic_getter = GetLatestPic(tempfilename)

app = FastAPI()

@app.get("/")
async def read_root():
    return {"Hello","World"}

# /latest_pic?width=1920&height=1080
@app.get("/latest_pic")
def latest_pic_selenium(width:int,height:int):
    path = pic_getter.get_latest_pic_from_url_selenium(url,width,height)
    return FileResponse(str(path))



# uvicorn server:app --reload