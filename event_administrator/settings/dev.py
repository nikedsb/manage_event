import os

from .base import *  # noqa: F401,F403
from .utils import strtobool

DEBUG = strtobool(os.getenv("DEBUG", "y"))
