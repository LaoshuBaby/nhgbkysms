import csv
import io
import os
import random
from datetime import datetime
from typing import Dict, List, Optional

import requests
import uvicorn
from fastapi import FastAPI, File, HTTPException, Path, Response
from fastapi.responses import FileResponse, HTMLResponse

from logger import nya

app = FastAPI()
nya(msg="[start] nhgbkysms",path="/nhgbkysms")


BASE_URL = "https://laoshubaby.oss-cn-beijing.aliyuncs.com/static/nihongo/nhgbkysms.lock"
ENDPOINT = {
    "cn": "http://fastapi-64cd.fcv3.1377713435577244.cn-qingdao.fc.devsapp.net/",
    "global": "http://nhgbkysms.zeabur.app/",
}


def get_resource_url(dictbook: str, collection: str) -> str:
    return BASE_URL.replace("nhgbkysms.lock", "") + dictbook + "/" + collection


def get_tango(uri: str = "") -> str:
    if type(uri) == type("str"):
        if uri[0:4] == "http":
            r = requests.get(url=uri)
            return r.content.decode("utf-8")
        else:
            pass
    else:
        print(".")


def parse_tango(
    dictbook: str = "dictbook", collection: str = "collection"
) -> List[Optional[Dict[str, str]]]:
    if (dictbook == "" or dictbook == "dictbook") or (
        collection == "" or collection == "collection"
    ):
        content = get_tango(
            uri=get_resource_url(
                "minnanonihongo.fltrp.shokyuu1", "tango.1.csv"
            )
        )
    else:
        content = get_tango(uri=get_resource_url(dictbook, collection))

    csv_file = io.StringIO(content)

    tango_all = []
    reader = csv.DictReader(csv_file)
    for row in reader:
        tango_all.append(row)

    return tango_all


def get_tango_list(mode: str = "local", collection: str = "") -> List[str]:
    if mode == "local":
        return os.listdir(
            os.path.join(os.path.dirname(__file__), "data", "tango")
        )
    if mode == "network":
        return []


@app.get("/")
async def hello():
    return {
        "time": datetime.now().astimezone().isoformat(),
        "note": "Hello World!",
    }


@app.get("/favicon.ico", response_class=FileResponse)
async def favicon():
    return FileResponse(
        path=os.path.join(os.path.dirname(__file__), "static", "favicon.ico")
    )


@app.get("/random/number/{number_range}")
async def read_random_number(
    number_range: int = Path(
        ...,
        description=(
            "The maximum value for the random number generation."
            "If not provided, the default is 100."
        ),
        ge=1,
    )
):
    max_value = number_range if number_range else 100

    random_number = random.randint(1, max_value)
    return {
        "random_number": random_number,
        "note": f"Random number between 1 and {max_value}.",
    }


@app.get("/tango/{unit}/{num}")
async def random_select_word(unit: str, num: int):
    if unit:
        if unit == "test" or unit == "testcase":
            tango_all: List[Optional[tuple]] = [
                {"romanji": "moji", "kanji": "文字", "hiragana": "もじ"},
                {"romanji": "ningen", "kanji": "人間", "hiragana": "にんげん"},
                {"romanji": "sakura", "kanji": "桜", "hiragana": "さくら"},
                {"romanji": "tsuki", "kanji": "月", "hiragana": "つき"},
                {"romanji": "hoshi", "kanji": "星", "hiragana": "ほし"},
            ]
        else:
            tango_all: List[Optional[Dict[str, str]]] = []
            if unit == "minnanonihongo":
                tango_all = parse_tango(
                    dictbook="minnanonihongo.fltrp.shokyuu1",
                    collection="tango.6.csv",
                )
            else:
                return {"warning": "invalid unit"}

        if num > len(tango_all):
            raise HTTPException(
                status_code=400,
                detail="Number of words requested exceeds available words.",
            )

        tango_list = random.sample(tango_all, num)

        return {"unit": unit, "tango_list": tango_list}
    else:
        return {"warning": "without unit"}


@app.get("/about")
async def about():
    with open(
        os.path.join(os.path.dirname(__file__), "pages", "about.html"),
        "r",
        encoding="utf-8",
    ) as f:
        return HTMLResponse(f.read())


@app.get("/dashboard")
async def about():
    with open(
        os.path.join(os.path.dirname(__file__), "pages", "result.html"),
        "r",
        encoding="utf-8",
    ) as f:
        return HTMLResponse(
            f.read().replace("{{{endpoint}}}", ENDPOINT["global"])
        )


@app.get("/result")
async def about():
    with open(
        os.path.join(os.path.dirname(__file__), "pages", "result.html"),
        "r",
        encoding="utf-8",
    ) as f:
        return HTMLResponse(f.read().replace("{{{endpoint}}}", ENDPOINT["cn"]))


@app.get("/status/tango")
async def about():
    return {"dict_count": int(len(get_tango_list()))}


@app.get("/status/listdir")
async def about():
    return {"dict_count": os.listdir()}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9000)
