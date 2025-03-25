import datetime
from applications.init import db


class Tag(db.Model):
    __tablename__ = 'magic_tag'
    id = db.Column(db.Integer, primary_key=True, comment="标签ID")
    parent_id = db.Column(db.Integer, comment="父级编号")
    dept_id = db.Column(db.Integer, comment="所属企业")
    tag_name = db.Column(db.String(50), comment="标签名称")
    tag_descript = db.Column(db.String(50), comment="标签描述")
    status = db.Column(db.Integer, comment='状态(1开启,0关闭)')
    remark = db.Column(db.Text, comment="备注")
    create_at = db.Column(db.DateTime, default=datetime.datetime.now, comment='创建时间')
    update_at = db.Column(db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now, comment='创建时间')