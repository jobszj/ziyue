
# 第三方接口的URL
LOCAL_MJ__URL = 'http://127.0.0.1:8989/mj/submit/imagine'
TENCENT_MJ_URL = 'http://119.91.238.87/mj/submit/imagine'

def mj_generate_image(args):
    prompt = args.get('prompt')
    img = args.get('imageUrl')
    if img:
        # 将图片地址转化为base64

        # 图生图
        payload = {
            "prompt": prompt,
            "base64Array":  ,
            "base64":
        }
    else:
        # 文生文
