#调用mj服务""
import asyncio

from applications.core.midjourney.api.mj_api import submit_imagine
from applications.core.midjourney.entity.mj_scheme import ImagineRequest

prompt = ImagineRequest(
    mode="RELAX",
    notify_hook="http://ziyuex.uicp.cn:40416/magic/image/callback",
    imgs=[],
    prompt="a girl")
print(asyncio.run(submit_imagine(prompt)))
