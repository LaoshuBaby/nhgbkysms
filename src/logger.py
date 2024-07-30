import os
from datetime import datetime 
import opendal

S3_BUCKET="laoshubaby"
S3_REGION="cn-beijing"
S3_ENDPOINT="https://laoshubaby.oss-cn-beijing.aliyuncs.com"

def init_operator() -> opendal.Operator:
    """
    假定用户已经配置过aliyun-python-sdk
    """
    return opendal.Operator(
        scheme="s3",
        root="/",
        bucket=S3_BUCKET,
        region=S3_REGION,
        endpoint=S3_ENDPOINT,
        access_key_id=os.environ.get("ALIYUN_ACCESSKEY_ID", ""),
        secret_access_key=os.environ.get("ALIYUN_ACCESSKEY_SECRET", ""),
        enable_virtual_host_style="True",
    )


def get_file(op: opendal.Operator, path: str) -> str:
    content = op.read(path)
    return content.decode("utf-8")

def set_file(op: opendal.Operator, path: str, content:str):
    op.write(path, content.encode('utf-8'))

op = init_operator()
set_file(op,"/static/nihongo/nhgbkysms.metadata.json1",str(datetime.now()))
file_content = get_file(op, "/static/nihongo/nhgbkysms.metadata.json")
print(file_content)
