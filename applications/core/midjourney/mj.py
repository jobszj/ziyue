import requests

MJ_IMAGE_URL="http://127.0.0.1:8989/mj/submit/imagine"
MJ_UPSCALE_URL="http://127.0.0.1:8989/mj/submit/change"

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

def txt_image_mj(prompt_en, taskid):
    pro = {
        "prompt": prompt_en,
        "state": taskid
    }
    response = requests.post(MJ_IMAGE_URL, json=pro)
    print(response)

def image_image_mj(prompt_en, goods_pic, taskid):
    pro = {
        "prompt": prompt_en,
        "base64": goods_pic,
        "state": taskid,
    }
    response = requests.post(MJ_IMAGE_URL, json=pro)
    print(response)

def mj_image_upscale(taskid, index):
    pro = {
        "taskId": taskid,
        "action": "UPSCALE",
        "index": index
    }
    response = requests.post(MJ_IMAGE_URL, json=pro)

    print(response, response.json().get("imageUrl"))


if __name__ == '__main__':
    txt_image_mj("a girl", "12345")