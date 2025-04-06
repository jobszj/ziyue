import http.client
import json

# 定义 API 密钥和基本 URL
API_KEY = "sk-R2ZImE064EXxP1LuLDpiZyIWkqGKI70B1iWsw6Mk8xU25x8C"  # 请替换为你的 DMXAPI 令牌
API_HOST = "www.dmxapi.cn"  # API 主机地址
API_ENDPOINT = "/v1/images/generations"  # API 请求路径

# 请求参数
prompt_text = "concept art of beautiful victorian princess, poldark, poldark, elizabeth Warleggan, megan fox, claire fraser, outlander, victorian woman in forest farm, black loose hair, tan skin, blue eyes, long voluminous flowing black loose hair, rapunzel black hair, very long waist length flowing loose dark black hair, realistic illustration, sabine rich, artgerm, j scott campbell, perfect body, detailed, intricate, round face, slim nose, black eyelashes, pink lips, sharp jawline, womanly hourglass figure, perfect detailed face, cinematic, full body, full body outfit view, flower forest cottage background, princess, formal long corset dress, tight fitted 3/4 sleeves, ribbons, tight sleeves, princess, realistic illustration, house of cb corset, low cut plunging neckline, marie Antoinette, tight fitted bell lace trim sleeves, white dainty diamond pendant necklace and earrings, diamonds, red satin silk embroidered pattern fabric, huge skirt, red ball gown, sequin tulle, glitter, sequin skirt"  # 描述生成图像的提示词
model_name = "dall-e-3"  #  除了dall-e-3 还可选：flux-schnell,flux-dev,flux.1.1-pro
image_size = "1024x1024"  # 图像尺寸 参考值：1792x1024, 1024 × 1792, 1024x1024

# 构建请求的 JSON 数据
payload = json.dumps(
    {
        "prompt": prompt_text,
        "n": 1,  # 生产图片数量，修改会报错，默认1就可以。
        "model": model_name,
        "size": image_size,
    }
)

# 定义请求头信息
headers = {
    "Authorization": f"Bearer {API_KEY}",  # 使用变量 API_KEY
    "Accept": "application/json",
    "User-Agent": "DMXAPI/1.0.0 (https://www.dmxapi.cn)",
    "Content-Type": "application/json",
}

# 建立 HTTPS 连接
conn = http.client.HTTPSConnection(API_HOST)

# 发送 POST 请求
conn.request("POST", API_ENDPOINT, payload, headers)

# 获取响应并读取数据
res = conn.getresponse()
data = res.read()

# 输出结果
print(data.decode("utf-8"))