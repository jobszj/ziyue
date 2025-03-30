import datetime
from applications.init import db


class Tasks(db.Model):
    __tablename__ = 'magic_task'
    id = db.Column(db.Integer, primary_key=True, comment="任务ID自增")
    task_id = db.Column(db.String(100), comment="任务ID")
    task_type = db.Column(db.String(20), comment="任务类型（txt2img,img2img,txt2vid.img2vid,vid2vid）")
    prompt = db.Column(db.Text, comment="用户输入的提示词")
    quantity = db.Column(db.Integer, comment="数量")
    task_model = db.Column(db.String(20), comment="模型名称")
    goods_pic = db.Column(db.String(255), comment="商品图片")
    status = db.Column(db.String(10), comment='任务的状态（Pending，Running，Completed，Failed）')
    user_id = db.Column(db.Integer, comment="用户ID")
    user_name = db.Column(db.String(50), comment="用户名")
    finish_at = db.Column(db.DateTime, comment="完成时间")
    create_at = db.Column(db.DateTime, default=datetime.datetime.now, comment='创建时间')
    update_at = db.Column(db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now, comment='创建时间')