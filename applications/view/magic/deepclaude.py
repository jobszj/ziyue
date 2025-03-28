from flask import Blueprint, render_template, request
from applications.core.deepclaude.manager import model_manager

bp = Blueprint('deepclaude', __name__, url_prefix='/deepclaude')

# 脚本生成
@bp.get('/')
def main():
    return render_template("deepclaude/index.html")

# 生成图片表单提交功能接口
@bp.route('/v1/chat/completions', methods=['POST'])
def completions():
    body = request.get_json(force=True)
    # 创建任务，并直接返回，服务端通过多线程方式实现多任务
    return model_manager.process_request(body)


@bp.get("/v1/models")
async def list_models():
    """获取可用模型列表

    使用 ModelManager 获取从配置文件中读取的模型列表
    返回格式遵循 OpenAI API 标准
    """
    try:
        models = model_manager.get_model_list()
        return {"object": "list", "data": models}
    except Exception as e:
        return {"error": str(e)}


@bp.get("/v1/config")
def get_config():
    """获取模型配置

    返回当前的模型配置数据
    """
    try:
        # 使用 ModelManager 获取配置
        config = model_manager.get_config()
        return config
    except Exception as e:
        return {"error": str(e)}


@bp.post("/v1/config")
def update_config():
    """更新模型配置

    接收并保存新的模型配置数据
    """
    try:
        # 获取请求体
        body = request.json()
        # 使用 ModelManager 更新配置
        model_manager.update_config(body)

        return {"message": "配置已更新"}
    except Exception as e:
        return {"error": str(e)}


