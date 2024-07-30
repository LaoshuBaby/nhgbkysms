import time
from datetime import datetime, timezone

from storage import get_file, init_operator, set_file

default_path = "/log"

op = init_operator()


def get_utc_timestamp():
    now_utc = datetime.now(timezone.utc)
    formatted_time = now_utc.isoformat(timespec="seconds").replace(
        "+00:00", "Z"
    )
    return (
        formatted_time.replace(":", "-")
        .replace("-", "-")
        .replace("T", "_")
        .replace("Z", "")
    )


def get_log_file_name():
    return get_utc_timestamp() + ".log"


def meow():
    trash=get_file(op, "/static/nihongo/nhgbkysms.metadata.json")
    print(trash)
    return trash


def nya(msg: str, level:str="INFO", path: str = ""):
    content=f"[{level}]"
    if len(path) > 0:
        if path[0] != "/":
            print("path should start with /")
            return None
    set_file(op, default_path + path + "/" + get_log_file_name(), content)