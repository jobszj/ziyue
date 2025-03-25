from enum import Enum

class Model(Enum):
    SD = "stablediffusion"
    MD = "midjunery"

class MediaType(Enum):
    i = 'image'
    s = 'sound'
    v = 'video'
    u = 'upload'