import os
from flask import Blueprint, request, render_template, jsonify, current_app

from applications.common.qiniu import upload_image_to_qiniu
from applications.common.utils.http import fail_api, success_api, table_api
from applications.common.utils.rights import authorize
from applications.service.aigc import upload as upload_curd

bp = Blueprint('adminFile', __name__, url_prefix='/file')


#  图片管理
@bp.get('/')
@authorize("system:file:main")
def index():
    return render_template('system/photo/photo.html')


#  图片数据
@bp.get('/table')
@authorize("system:file:main")
def table():
    page = request.args.get('page', type=int)
    limit = request.args.get('limit', type=int)
    data, count = upload_curd.get_aigc(page=page, limit=limit)
    return table_api(data=data, count=count)


@bp.post('/uploadqn')
@authorize("system:file:add", log=True)
def upload_qiniu_api():
    if 'file' in request.files:
        photo = request.files['file']

        # 将图片转换成base64然后上传到七牛云
        photo_data = photo.read()
        file_url = upload_image_to_qiniu(photo_data, 'u')
        res = {
            "msg": "上传成功",
            "code": 0,
            "success": True,
            "data":
                {"src": file_url}
        }
        return jsonify(res)
    return fail_api()


#    图片删除
@bp.route('/delete', methods=['GET', 'POST'])
@authorize("system:file:delete", log=True)
def delete():
    _id = request.form.get('id')
    res = upload_curd.delete_photo_by_id(_id)
    if res:
        return success_api(msg="删除成功")
    else:
        return fail_api(msg="删除失败")

