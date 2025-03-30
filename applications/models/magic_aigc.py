import datetime
from applications.init import db


class Aigc(db.Model):
    __tablename__ = 'magic_aigc'
    id = db.Column(db.Integer, primary_key=True, comment="任务ID自增")
    task_id = db.Column(db.String(100), comment="任务ID")
    prompt_zh = db.Column(db.Text, comment="用户输入的提示词")
    prompt_en = db.Column(db.Text, comment="优化后的英文提示词")
    neg_prompt = db.Column(db.Text, comment="反向提示词")
    aigc_url = db.Column(db.String(255), comment="生成的内容链接")
    create_at = db.Column(db.DateTime, default=datetime.datetime.now, comment='创建时间')
