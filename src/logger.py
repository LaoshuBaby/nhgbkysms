import os
import sys
import opendal


def init_environ():
    """
    假定用户已经配置过aliyun-python-sdk
    """
    ALIYUN_ACCESSKEY_ID = os.environ.get("ALIYUN_ACCESSKEY_ID", "")
    ALIYUN_ACCESSKEY_SECRET = os.environ.get("ALIYUN_ACCESSKEY_SECRET", "")
    os.environ["AWS_ACCESS_KEY_ID"] = ALIYUN_ACCESSKEY_ID
    os.environ["AWS_SECRET_ACCESS_KEY"] = ALIYUN_ACCESSKEY_SECRET


def init_operator() -> opendal.Operator:
    return opendal.Operator(
        scheme="s3",
        root="/",
        bucket="laoshubaby",
        region="cn-beijing",
        endpoint="https://laoshubaby.oss-cn-beijing.aliyuncs.com",
        enable_virtual_host_style="True",
    )


def get_file(op: opendal.Operator, path: str) -> str:
    content = op.read(path)
    return content.decode("utf-8")


init_environ()
op = init_operator()
file_content = get_file(op, "/static/nihongo/nhgbkysms.metadata.json")
print(file_content)
