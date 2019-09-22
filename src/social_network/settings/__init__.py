from .django import *
from .rest_settings import *


try:
    from settings_local import *
except ImportError:
    pass
