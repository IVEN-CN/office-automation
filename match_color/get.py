import csv
from multiprocessing import shared_memory
import os
from smb.SMBConnection import SMBConnection
import time

def main(path:str):
    data_pass = []
    with open('已通过.csv','r') as f:
        reader = csv.reader(f)
        for row in reader:
            data_pass.append(row[0])

    # 获取path路径下的所有文件，包括文件夹下的文件
    filenames = get_local_file_name(path)
    for filename in filenames:
        for data in data_pass:
            if data[-4:] not in filename:
                print(f'{data}未使用过')

def get_local_file_name(path:str):
    """获取本地文件夹下所有文件名"""
    path_list = []
    for dirpath, dirnames, filenames in os.walk(path):
        for filename in filenames:
            path_list.append(filename)
    return path_list

def get_smb_file_name(path:str):
    """获取smb文件夹下所有文件名"""
    # 连接smb
    host = '192.168.5.66'
    username = 'Administrator'
    password = ''
    conn = SMBConnection(username, password, 'PC-IVEN', 'hzrc-01', use_ntlm_v2=True)
    while 1:
        try:
            assert conn.connect(host, 139)
            break
        except:
            time.sleep(2)
            continue

    # 获取文件名
    file_list = []
    share = '瑞诚服装设计组可更改'
    for file_info in conn.listPath(share, path):   # path是以'/'开头的路径
        if file_info.filename in ['.', '..']:
            continue
        if file_info.isDirectory:  # 如果是目录，递归调用
            sub_path = path
            if not sub_path.endswith('/'):
                sub_path += '/'
            sub_path += file_info.filename
            file_list.extend(get_smb_file_name(sub_path))
        else:  # 如果是文件，添加到列表
            file_list.append(file_info.filename)
    return file_list

if __name__ == '__main__':
    # lst = get_smb_file_name('PNG格式P图图案')
    lst = get_smb_file_name('PNG格式P图图案/23春夏PNG')
    print(lst)