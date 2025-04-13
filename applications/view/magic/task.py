from flask import Blueprint, render_template
from sqlalchemy import desc

from applications.common.utils.http import table_api
from applications.common.utils.rights import authorize
from applications.models import Tasks
from applications.schemas.magic_task import TaskSchema

bp = Blueprint('task', __name__, url_prefix='/task')


@bp.get('/')
@authorize("magic:task:main", log=True)
def main():
    return render_template("magic/task/main.html")


@bp.get('/data')
@authorize("magic:task:main", log=True)
def data():
    try:
        tasks = Tasks.query.order_by(desc(Tasks.create_at)).all()
        return table_api(data=TaskSchema(many=True).dump(tasks))
    except Exception as e:
        print(e)
        return table_api(msg=str(e))
