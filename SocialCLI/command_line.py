from .utils import (mkdir, Dispatch, DATA_DIR)


def start():
    mkdir(DATA_DIR)
    Dispatch()
