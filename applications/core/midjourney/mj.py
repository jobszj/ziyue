import requests

# 第三方接口的URL
DMX_MJ_IMAGE_URL = 'https://www.dmxaip.com/mj/submit/imagine'
DMX_MJ_IMAGE_UPSCALE = 'https://www.dmxaip.com/mj/submit/imagine'
DMX_API_KEY = "sk-EDxfLAotJ89hilXDHE863vVfXkwEljOlH0zKmY46HZ8W8siw"


def dmx_mj_generate_image(args):
    args = {
        "mode": "FAST",
        "notifyHook": "",
        "base64Array": [],
        "expand": args.get("prompts"),   #提示词用英文
        "state": ""
    }

    headers = {
        'Accept': 'application/json',
        'Authorization': DMX_API_KEY,
        'User-Agent': 'DMXAPI/1.0.0 (https://www.dmxapi.cn)',
        'Content-Type': 'application/json'
    }

    try:
        # 调用第三方接口
        response = requests.post(url=DMX_MJ_IMAGE_URL, json=args, headers=headers)
        response.raise_for_status()  # 如果响应状态码不是200，会抛出异常
        # 解析响应数据
        data = response.json()

        print("返回的结果", data)
    except requests.exceptions.RequestException as e:
        # 处理请求异常
        return print(str(e)), 500

# 第三方接口的URL
DISCORD_MJ_IMAGE_URL = "127.0.0.1:7860/"


def discord_mj_generate_image(prompt_en):
    # 调用第三方接口
    pass