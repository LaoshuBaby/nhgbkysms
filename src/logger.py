import inspect
import os
import time
from datetime import datetime, timezone

from storage import get_file, init_operator, set_file

default_path = "/log"

op = init_operator()


def frame_info():
    frame_current = inspect.currentframe()
    frame_caller = frame_current.f_back
    info_filename = os.path.basename(frame_caller.f_code.co_filename)
    info_lineno = frame_caller.f_lineno
    info_funcname = frame_caller.f_code.co_name

    return f"{info_filename}:{info_funcname}:{info_lineno}"


def get_utc_timestamp():
    now_utc = datetime.now(timezone.utc)
    formatted_time = now_utc.isoformat(timespec="milliseconds").replace(
        "+00:00", "Z"
    )
    return formatted_time


def get_log_file_name(data: str = None):
    def get_safe_name(data: str) -> str:
        return (
            data.replace(":", "-")
            .replace("-", "-")
            .replace("T", "_")
            .replace("Z", "")
        )

    if data:
        if data[-4:] != ".log":
            return get_safe_name(data) + ".log"
        else:
            return get_safe_name(data)
    else:
        return get_safe_name(data) + ".log"


def meow():
    trash = get_file(op, "/static/nihongo/nhgbkysms.metadata.json")
    print(trash)
    return trash


def nya(
    msg: str,
    path: str = "",
    time: str = get_utc_timestamp(),
    level: str = "INFO",
    func: str = "",
):
    content = f"{time} | {level} | {func} - {msg}"
    if len(path) > 0:
        if path[0] != "/":
            print("path should start with /")
            return None
    set_file(op, default_path + path + "/" + get_log_file_name(time), content)
