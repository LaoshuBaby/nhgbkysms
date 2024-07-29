import os
import opendal

# 设置阿里云OSS凭证
os.environ['AWS_ACCESS_KEY_ID'] = ''
os.environ['AWS_SECRET_ACCESS_KEY'] = ''

# 初始化 S3 操作符
op = opendal.Operator(
    scheme="s3",
    root="/",
    bucket="laoshubaby",
    region="cn-beijing",
    endpoint="https://laoshubaby.oss-cn-beijing.aliyuncs.com",
    enable_virtual_host_style="True",
)

# 读取文件内容
file_content = op.read("/static/nihongo/nhgbkysms.metadata.json1")
print(file_content.decode('utf-8'))