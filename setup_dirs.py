import os

dirs = [
    'src',
    'src/models',
    'src/ui',
    'src/utils',
    'src/config',
    'tests'
]

for d in dirs:
    os.makedirs(d, exist_ok=True)
