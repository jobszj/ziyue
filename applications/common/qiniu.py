import base64
import os
import tempfile
import uuid
from datetime import datetime

import requests
from qiniu import Auth, put_file, etag, put_data

access_key = 'IKEXJpB1KnHukAQJsfRDJOkzUW5b2QF_g0DmrwT_'
secret_key = 'sXRou32y4Go1YKHTUwZk82Vyqyst7sl5TAsfb69V'
#要上传的空间
bucket_name = 'ziyuex'
#构建鉴权对象
q = Auth(access_key, secret_key)
#生成上传 Token，可以指定过期时间等
token = q.upload_token(bucket_name)

def upload_image_to_qiniu(base64_data, type = 'g'):
    random_filename = f"{uuid.uuid4().hex}.png"
    # 获取当前日期
    current_date = datetime.now().strftime('%Y/%m/%d')
    # 生成上传路径
    if type == 'g':
        key = f'magic/sdlt/{current_date}/{random_filename}'
    elif type == 'mj':
        key = f'magic/midjourney/{current_date}/{random_filename}'
    else:
        key = f'magic/upload/{current_date}/{random_filename}'
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


def upload_image_to_qiniu_by_url(url, type = 'g'):
    random_filename = f"{uuid.uuid4().hex}.png"
    # 获取当前日期
    current_date = datetime.now().strftime('%Y/%m/%d')
    # 生成上传路径
    if type == 'g':
        key = f'magic/sdlt/{current_date}/{random_filename}'
    elif type == 'mj':
        key = f'magic/midjourney/{current_date}/{random_filename}'
    else:
        key = f'magic/upload/{current_date}/{random_filename}'
    # 下载图片
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception("下载图片失败")
    # 上传到七牛云
    ret, info = put_data(token, key, response.content)

    # 处理结果
    if info.status_code == 200:
        pic_url = f'https://pics.ziyuex.com/' + key
        # 返回图片URL
        return pic_url
    else:
        print("上传失败！错误信息:", info)


def convert_url_to_data_url(url):
    try:
        # 1. 下载图片
        response = requests.get(url)
        response.raise_for_status()

        # 2. 获取 MIME 类型（通过 URL 扩展名）
        mime_type = "image/jpeg"  # 默认值
        if url.lower().endswith(".png"):
            mime_type = "image/png"
        elif url.lower().endswith(".gif"):
            mime_type = "image/gif"

        # 3. 生成 Base64
        base64_data = base64.b64encode(response.content).decode("utf-8")
        return f"data:{mime_type};base64,{base64_data}"
    except Exception as e:
        print(f"转换失败: {e}")
        return None
