from applications.init import ma
from marshmallow import fields


class AigcOutSchema(ma.Schema):
    id = fields.Integer()
    task_id = fields.Str()
    sub_task_id = fields.Str()
    sub_task_tags = fields.Str()
    aigc_url = fields.Str()
    prompt_zh = fields.Str()
    prompt_en = fields.Str()
    create_at = fields.DateTime()
