import requests

MJ_IMAGE_URL="http://127.0.0.1:8989/mj/submit/imagine"

# 发起请求
def send_request():
    imgurl = "https://pics.ziyuex.com/magic/upload/2025/03/30/c9d04f277426410497e5824aee130bcf.png"

    pro = {
        # "prompt": "The kettle comes from the uploaded picture. Without modifying any information about the kettle, place the kettle on the stove to boil water. Be sure not to modify the information of the kettle in the picture.",
        "prompt": "a girl",
        "base64Array": [imgurl],
        "base64": "",
        "notifyHook": ""
    }
    response = requests.post(MJ_IMAGE_URL, json=pro)
    #
    if response.status_code == 200:
        print(response.json())
    else:
        print(response.text)

def txt_image_mj(prompt_en):
    pro = {
        "prompt": prompt_en,
        "base64Array": "",
        "base64": "",
        "state": "",
        "notifyHook": ""
    }
    response = requests.post(MJ_IMAGE_URL, json=pro)
    print(response)
    pass

def image_image_mj(prompt_en, goods_pic):
    pro = {
        "prompt": prompt_en,
        "base64Array": "",
        "base64": goods_pic,
        "state": "",
        "notifyHook": ""
    }
    response = requests.post(MJ_IMAGE_URL, json=pro)
    print(response)
    pass