import base64
from PIL import Image
import io
from flask import jsonify
import requests

from applications.common.qiniu import upload_image_to_qiniu
from applications.common.utils.http import success_api, fail_api, table_api

# 第三方接口的URL
LOCAL_API_URL = 'http://127.0.0.1:7860/sdapi/v1/'
TENCENT_API_URL = 'http://119.91.238.87/sdapi/v1/'

def image_sdlt(args):
    prompt = args.get('prompt')
    img = args.get('imageUrl')
    if not img:
        # 调用文生图
        url = LOCAL_API_URL + 'txt2img'
        payload = {
            "prompt": prompt,
            "steps": 20,
            "batch_size": 1,
            "cfg_scale": 7,
            "denoising_strength": 0,
            "enable_hr": False,
            "eta": 0,
            "firstphase_height": 0,
            "firstphase_width": 0,
            "n_iter": 1,
            "negative_prompt": "",
            "restore_faces": False,
            "s_churn": 0,
            "s_noise": 1,
            "s_tmax": 0,
            "s_tmin": 0,
            "sampler_index": "Euler a",
            "seed": -1,
            "seed_resize_from_h": -1,
            "seed_resize_from_w": -1,
            "styles": [],
            "subseed": -1,
            "subseed_strength": 0,
            "tiling": False,
            "height": 512,
            "width": 512
        }
    else:
        # 调用图生图
        url = LOCAL_API_URL + 'img2img'
        # 根据图片链接获取图片base64
        # 从图片链接下载图片
        response = requests.get(img)
        response.raise_for_status()
        image_data = response.content
        # 将图片数据转换为 Base64 编码
        base64_image = base64.b64encode(image_data).decode('utf-8')
        payload = {
            "batch_size": 1,
            "cfg_scale": 7,
            "denoising_strength": 0.75,
            "eta": 0,
            "height": 512,
            "include_init_images": False,
            "init_images": [base64_image],
            "inpaint_full_res": False,
            "inpaint_full_res_padding": 0,
            "inpainting_fill": 0,
            "inpainting_mask_invert": False,
            "mask": None,
            "mask_blur": 4,
            "n_iter": 1,
            "negative_prompt": "",
            "override_settings": {},
            "prompt": prompt,
            "resize_mode": 0,
            "restore_faces": False,
            "s_churn": 0,
            "s_noise": 1,
            "s_tmax": 0,
            "s_tmin": 0,
            "sampler_index": "Euler a",
            "seed": -1,
            "seed_resize_from_h": -1,
            "seed_resize_from_w": -1,
            "steps": 20,
            "styles": [],
            "subseed": -1,
            "subseed_strength": 0,
            "tiling": False,
            "width": 512
        }
    try:
        # 调用第三方接口
        response = requests.post(url=url, json=payload)
        print("调用接口", response, prompt)
        # 检查响应状态
        if response.status_code == 200:
            data = response.json()
            if 'images' in data and len(data['images']) > 0:
                # 解码Base64字符串
                image_data = base64.b64decode(data['images'][0])
                # 将图片上传至七牛云，并返回图片URL
                pic_url = upload_image_to_qiniu(image_data, 'g')
                # 将二进制数据转换为图像对象
                image = Image.open(io.BytesIO(image_data))
                # 定义图片保存路径
                image.save(f"image222.png")
                # 这里可以处理返回的图像数据
                return pic_url
            else:
                return fail_api(msg="响应中没有找到图像数据")
    except requests.exceptions.RequestException as e:
        # 处理请求异常
        print(f"生成失败: {str(e)}")
        return fail_api(msg=f"生成失败: {str(e)}")


def txt2img_tencent():
    args = {
        "prompt": "a girl in a park",
        "negative_prompt": "longbody, lowres, bad anatomy, bad hands, missing fingers, extra digit, fewer digits, cropped, worst quality, low quality",
        "steps": 20,
        "width": 258,
        "height": 258,
        "seed": 0,
        "guidance_scale": 7.5,
    }
    url = "/txt2img"
    try:
        # 调用第三方接口
        response = requests.post(url=TENCENT_API_URL + url, json=args)
        response.raise_for_status()  # 如果响应状态码不是200，会抛出异常
        # 解析响应数据
        data = response.json()
        # 返回响应给客户端
        return jsonify(data), 200
    except requests.exceptions.RequestException as e:
        # 处理请求异常
        return jsonify({'error': str(e)}), 500


def script_tencent():
    url = "/scripts"
    try:
        # 调用第三方接口
        response = requests.post(url=TENCENT_API_URL + url)
        response.raise_for_status()  # 如果响应状态码不是200，会抛出异常
        # 解析响应数据
        data = response.json()
        print("返回的结果", jsonify(data))
        # 返回响应给客户端
        return 200
    except requests.exceptions.RequestException as e:
        # 处理请求异常
        return jsonify({'error': str(e)}), 500


def script_local():
    url = "/scripts"
    try:
        # 调用第三方接口
        response = requests.post(url= LOCAL_API_URL + url)
        response.raise_for_status()  # 如果响应状态码不是200，会抛出异常
        # 解析响应数据
        data = response.json()
        print("返回的结果", jsonify(data))
        # 返回响应给客户端
        return 200
    except requests.exceptions.RequestException as e:
        # 处理请求异常
        return jsonify({'error': str(e)}), 500
