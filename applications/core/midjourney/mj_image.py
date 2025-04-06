import requests

MJ_IMAGE_URL="http://127.0.0.1:8989/mj/submit/imagine"

# 发起请求
def send_request():
    url = MJ_IMAGE_URL
    imgurl = "https://pics.ziyuex.com/magic/upload/2025/03/30/c9d04f277426410497e5824aee130bcf.png"

    pro = {
        # "prompt": "The kettle comes from the uploaded picture. Without modifying any information about the kettle, place the kettle on the stove to boil water. Be sure not to modify the information of the kettle in the picture.",
        "prompt": "a girl",
        "base64Array": [imgurl],
        "base64": "",
        "notifyHook": ""
    }
    response = requests.post(url, json=pro)
    #
    if response.status_code == 200:
        print("请求成功")
        print(response.json())
    else:
        print("请求失败")
        print(response.status_code)
        print(response.text)


send_request()