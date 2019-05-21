import os

def path_type(path):
    if os.path.isdir(path):
        print('Dir')
    elif os.path.isfile(path):
        print('File')
    else:
        print('Other')

path1 = '/etc'
path2 = './README.md'
path3 = 'notexist'

path_type(path1)
path_type(path2)
path_type(path3)