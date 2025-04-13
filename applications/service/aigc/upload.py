from sqlalchemy import desc
from applications.init import db
from applications.models import Aigc
from applications.common.curd import model_to_dicts
from applications.schemas.admin_photo import AigcOutSchema


def get_aigc(page, limit):
    aigc = Aigc.query.order_by(desc(Aigc.create_at)).paginate(page=page, per_page=limit, error_out=False)
    count = Aigc.query.count()
    data = model_to_dicts(schema=AigcOutSchema, data=aigc.items)
    return data, count


def delete_photo_by_id(_id):
    photo_name = Aigc.query.filter_by(id=_id).first().name
    photo = Aigc.query.filter_by(id=_id).delete()
    db.session.commit()
    return photo
