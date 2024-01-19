"""主图文件夹里面同样要重命名，800(6)改成800(1),类似的，1000(6)改成1000(1),1200(6)改成1200(1)"""
import os
import re
try:
    import main1
except:
    import renamer.main1 as main1

def rename2(path):
    dir = path
    path_list = main1.get_file_path(dir)
    list_ = []

    for i in path_list:
        # v = int(i[-6])       # 取括号内的数字
        k = i
        num = re.search(r'\((\d+)\)', i).group(1)  # 取括号内的数字
        num_ = int(num)
        new_name = re.sub(r'\((\d+)\)', lambda match: f'({int(match.group(1))-5})', i)

        try:
            if '800' in i:
                os.rename(k, new_name)
            elif '1000' in i:
                os.rename(k, new_name)
            elif '1200' in i:
                os.rename(k, new_name)
        except:
            list_.append(i)

    for i in list_:
        k = i
        num = re.search(r'\((\d+)\)', i).group(1)  # 取括号内的数字
        num_ = int(num)
        new_name = re.sub(r'\((\d+)\)', lambda match: f'({int(match.group(1))-5})', i)

        if '800' in i:
            os.rename(k, new_name)
        elif '1000' in i:
            os.rename(k, new_name)
        elif '1200' in i:
            os.rename(k, new_name)

if __name__ == '__main__':
    rename2('D:\\41tm\\KC-41-XOU131\\main')