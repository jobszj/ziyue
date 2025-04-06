from flask import Blueprint, render_template, request, jsonify
from applications.common import curd
from applications.common.utils import validate
from applications.common.utils.http import success_api, fail_api
from applications.common.utils.rights import authorize
from applications.common.utils.validate import str_escape
from applications.init import db
from applications.models import User, Tag
from applications.schemas.magic_tag import TagSchema

bp = Blueprint('tag', __name__, url_prefix='/tag')


@bp.get('/')
@authorize("magic:tag:main", log=True)
def main():
    return render_template("magic/tag/main.html")


@bp.post('/data')
@authorize("magic:tag:main", log=True)
def data():
    data = Tag.query.order_by(Tag.sort).all()
    res = {
        "data": TagSchema(many=True).dump(data)
    }
    return jsonify(res)


@bp.get('/add')
@authorize("magic:tag:add", log=True)
def add():
    return render_template('magic/tag/add.html')


@bp.get('/tree')
@authorize("magic:tag:main", log=True)
def tree():
    tag = Tag.query.order_by(Tag.sort).all()
    tag_data = curd.model_to_dicts(schema=TagSchema, data=tag)
    res = {
        "status": {"code": 200, "message": "默认"},
        "data": tag_data

    }
    return jsonify(res)


@bp.post('/save')
@authorize("magic:tag:add", log=True)
def save():
    req_json = request.get_json(force=True)
    tag = Tag(
        parent_id=req_json.get('parentId'),
        tag_name=str_escape(req_json.get('TagName')),
        tag_descript=str_escape(req_json.get('tagDesc')),
        remark=str_escape(req_json.get('remark')),
        sort=str_escape(req_json.get('sort')),
        tag_status=str_escape(req_json.get('tagStatus'))
    )
    r = db.session.add(tag)
    db.session.commit()
    return success_api(msg="成功")


@bp.get('/edit')
@authorize("magic:tag:edit", log=True)
def edit():
    _id = request.args.get("tagId")
    tag = curd.get_one_by_id(model=Tag, id=_id)
    return render_template('magic/tag/edit.html', tag=tag)


# 启用
@bp.put('/enable')
@authorize("magic:tag:edit", log=True)
def enable():
    id = request.get_json(force=True).get('tagId')
    if id:
        enable = 1
        d = Tag.query.filter_by(id=id).update({"status": enable})
        if d:
            db.session.commit()
            return success_api(msg="启用成功")
        return fail_api(msg="出错啦")
    return fail_api(msg="数据错误")


# 禁用
@bp.put('/disable')
@authorize("magic:tag:edit", log=True)
def dis_enable():
    id = request.get_json(force=True).get('tagId')
    if id:
        enable = 0
        d = Tag.query.filter_by(id=id).update({"status": enable})
        if d:
            db.session.commit()
            return success_api(msg="禁用成功")
        return fail_api(msg="出错啦")
    return fail_api(msg="数据错误")


@bp.put('/update')
@authorize("magic:tag:edit", log=True)
def update():
    json = request.get_json(force=True)
    #id = json.get("deptId"),
    id = str_escape(json.get("tagId"))
    data = {
        "tag_name": validate.str_escape(json.get("tagName")),
        "tag_descript": validate.str_escape(json.get("tagDesc")),
        "remark": validate.str_escape(json.get("remark")),
        "sort": validate.str_escape(json.get("sort")),
        "tag_status": validate.str_escape(json.get("status"))
    }
    d = Tag.query.filter_by(id=id).update(data)
    if not d:
        return fail_api(msg="更新失败")
    db.session.commit()
    return success_api(msg="更新成功")


@bp.delete('/remove/<int:_id>')
@authorize("c", log=True)
def remove(_id):
    d = Tag.query.filter_by(id=_id).delete()
    if not d:
        return fail_api(msg="删除失败")
    res = User.query.filter_by(tag_id=_id).update({"tag_id": None})
    db.session.commit()
    if res:
        return success_api(msg="删除成功")
    else:
        return fail_api(msg="删除失败")
