import random
from datetime import datetime
from typing import List, Tuple

import uvicorn
from fastapi import FastAPI, HTTPException, Path
from fastapi.responses import HTMLResponse

app = FastAPI()


@app.get("/")
def hello():
    return {
        "time": datetime.now(datetime.timezone.utc).isoformat(),
        "note": "Hello World!",
    }


@app.get("/random/number/{number_range}")
async def read_random_number(
    number_range: int = Path(
        default=100,
        description="The max range value for the random number generation. Default is 100.",
        ge=1,
    )
):
    random_number = random.randint(1, number_range)
    return {
        "random_number": random_number,
        "note": f"Random number between 1 and {number_range}.",
    }


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


@app.get("/about")
async def about():
    with open("pages/about.html", "r", encoding="utf-8") as f:
        return HTMLResponse(f.read())


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9000)
