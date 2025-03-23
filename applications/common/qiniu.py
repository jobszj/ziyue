import os
import tempfile
import uuid
from datetime import datetime

from qiniu import Auth, put_file, etag

access_key = 'IKEXJpB1KnHukAQJsfRDJOkzUW5b2QF_g0DmrwT_'
secret_key = 'sXRou32y4Go1YKHTUwZk82Vyqyst7sl5TAsfb69V'
#要上传的空间
bucket_name = 'ziyuex'
#构建鉴权对象
q = Auth(access_key, secret_key)
#生成上传 Token，可以指定过期时间等
token = q.upload_token(bucket_name)

def upload_image_to_qiniu(base64_data):
    random_filename = f"{uuid.uuid4().hex}.png"
    # 获取当前日期
    current_date = datetime.now().strftime('%Y/%m/%d')
    # 生成上传路径
    key = f'magic/sdlt/{current_date}/{random_filename}'
    # 生成上传 Token，可以指定过期时间等
    token = q.upload_token(bucket_name, key, 3600)
    # 创建临时文件
    with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as temp_file:
        temp_file.write(base64_data)
        temp_file_path = temp_file.name

    try:
        # 使用 put_file 方法上传临时文件
        ret, info = put_file(token, key, temp_file_path, version='v2')
        print(info)
        assert ret['key'] == key
        assert ret['hash'] == etag(temp_file_path)

        pic_url = f'https://pics.ziyuex.com/' + key
        # 返回图片URL
        return pic_url

    finally:
        # 删除临时文件
        os.remove(temp_file_path)
