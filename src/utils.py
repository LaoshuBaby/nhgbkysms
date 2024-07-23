import os
from typing import Dict, List

from const import BASE_URL


def get_tango_list(mode: str = "local", collection: str = "") -> List[str]:
    if mode == "local":
        return os.listdir(
            os.path.join(os.path.dirname(__file__), "data", "tango")
        )
    if mode == "network":
        return []


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
