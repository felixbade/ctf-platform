import os
from pathlib import Path


def get_welcome():
    filename = os.path.join('puzzle', 'welcome.md')
    return open(filename).read()

def save_welcome(content):
    with open(os.path.join('puzzle', 'welcome.md'), 'w') as f:
        f.write(content)