import os
import random
from datetime import datetime
from typing import Dict, List, Optional

import uvicorn
from fastapi import FastAPI, HTTPException, Path
from fastapi.responses import FileResponse, HTMLResponse

from const import ENDPOINT
from utils import get_tango_list, parse_tango

app = FastAPI()


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
async def random_number(
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


@app.get("/tango/{dictbook}/{collection}/{num}")
async def tango(dictbook: str, collection: str, num: int):
    if dictbook:
        if ".csv" not in collection:
            collection += ".csv"
        if dictbook == "test" or dictbook == "testcase":
            tango_all: List[Optional[tuple]] = [
                {"romanji": "moji", "kanji": "文字", "hiragana": "もじ"},
                {"romanji": "ningen", "kanji": "人間", "hiragana": "にんげん"},
                {"romanji": "sakura", "kanji": "桜", "hiragana": "さくら"},
                {"romanji": "tsuki", "kanji": "月", "hiragana": "つき"},
                {"romanji": "hoshi", "kanji": "星", "hiragana": "ほし"},
            ]
        else:
            tango_all: List[Optional[Dict[str, str]]] = []
            if dictbook == "minnanonihongo":
                tango_all = parse_tango(
                    dictbook=dictbook,
                    collection=collection,
                )
            else:
                return {"warning": "invalid unit"}

        if num > len(tango_all):
            raise HTTPException(
                status_code=400,
                detail="Number of words requested exceeds available words.",
            )

        tango_list = random.sample(tango_all, num)

        return {"unit": dictbook, "tango_list": tango_list}
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
async def dashboard():
    # 这个函数后续会变为一站式的面板
    with open(
        os.path.join(os.path.dirname(__file__), "pages", "result.html"),
        "r",
        encoding="utf-8",
    ) as f:
        return HTMLResponse(
            f.read().replace("{{{endpoint}}}", ENDPOINT["global"])
        )


@app.get("/result")
async def result():
    with open(
        os.path.join(os.path.dirname(__file__), "pages", "result.html"),
        "r",
        encoding="utf-8",
    ) as f:
        return HTMLResponse(f.read().replace("{{{endpoint}}}", ENDPOINT["cn"]))


@app.get("/status/tango")
async def status_tango():
    return {"dict_count": int(len(get_tango_list()))}


@app.get("/status/listdir")
async def status_listdir():
    return {"dict_count": os.listdir()}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9000)
