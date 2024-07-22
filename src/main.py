import csv
import os
import random
from datetime import datetime
from typing import Dict, List, Optional

import uvicorn
from fastapi import FastAPI, File, HTTPException, Path, Response
from fastapi.responses import FileResponse, HTMLResponse

app = FastAPI()


def get_tango(uri: str = None) -> str:
    if uri[0:4] == "http":
        pass
    else:
        pass


def parse_tango() -> List[tuple]:
    return [(0)]


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
            if unit == "daiichika":
                with open(
                    os.path.join(
                        os.path.dirname(__file__),
                        "data",
                        "tango",
                        "daiichika.csv",
                    ),
                    mode="r",
                    newline="",
                    encoding="utf-8",
                ) as file:
                    reader = csv.DictReader(file)
                    for row in reader:
                        tango_all.append(row)
                # tango_all = parse_tango(
                #     dictbook="minnanonihongo.fltrp.shokyuu1", collection="6"
                # )
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


@app.get("/status/tango")
async def about():
    return {"dict_count": int(len(get_tango_list()))}


@app.get("/status/listdir")
async def about():
    return {"dict_count": os.listdir()}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9000)
