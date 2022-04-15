import os
from pathlib import Path


def get_welcome():
    filename = os.path.join('puzzle', 'welcome.md')
    return open(filename).read()
