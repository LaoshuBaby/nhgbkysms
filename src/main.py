import random
import datetime
from typing import List

import uvicorn
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()


@app.get("/")
def hello():
    return {
        "time": datetime.datetime.utcnow()
        .replace(tzinfo=datetime.timezone.utc)
        .isoformat(),
        "note": "Hello World!",
    }


@app.get("/random/number")
async def read_random_number():
    random_number = random.randint(1, 30)
    return {
        "random_number": random_number,
        "note": """""",
    }


@app.get("/about")
async def about():
    with open("pages/about.html", "r", encoding="utf-8") as f:
        return HTMLResponse(f.read())


from fastapi import FastAPI, HTTPException
from typing import List, Tuple
import random

app = FastAPI()


@app.get("/tango/{unit}/{num}")
async def random_select_word(unit: str, num: int):
    tango_all: List[Tuple[str, str, str]] = [
        ("moji", "文字", "もじ"),
        ("ningen", "人間", "にんげん"),
        ("sakura", "桜", "さくら"),
        ("tsuki", "月", "つき"),
        ("hoshi", "星", "ほし"),
    ]

    if num > len(tango_all):
        raise HTTPException(
            status_code=400,
            detail="Number of words requested exceeds available words.",
        )

    tango_list = random.sample(tango_all, num)

    return {"unit": unit, "tango_list": tango_list}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9000)
