import os

def mkdir(path):
    parent_dir = os.path.dirname(path)
    if not os.path.exists(parent_dir):
        mkdir(parent_dir)
    if not os.path.exists(path):
        os.mkdir(path)
