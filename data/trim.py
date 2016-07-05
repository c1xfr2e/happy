import os

rootdir = '/Users/zh/repo/history_ohlcv'
for name in os.listdir(rootdir):
    if not name.endswith('.txt'):
        continue
    pathname = os.path.join(rootdir, name)
    read_file = open(pathname)
    lines = read_file.readlines()
    read_file.close()
    w = open(pathname, 'w')
    w.writelines([item for item in lines[:-2]])
    w.close()
