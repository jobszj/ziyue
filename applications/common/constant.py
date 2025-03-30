from enum import Enum

class Model(Enum):
    SD = "SD"
    MJ = "MJ"

class MediaType(Enum):
    i = 'image'
    s = 'sound'
    v = 'video'
    u = 'upload'

class TaskStatus(Enum):
    PENDING = 'Pending'
    RUNNING = 'Running'
    COMPLETED = 'Completed'
    FAILED = 'Failed'

class TaskType(Enum):
    txt2img = 'txt2img'
    img2img = 'img2img'
    txt2vid = 'txt2vid'
    img2vid = 'img2vid'
    vid2vid = 'vid2vid'
