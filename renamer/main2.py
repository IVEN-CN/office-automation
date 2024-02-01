"""主图文件夹里面同样要重命名，800(6)改成800(1),类似的，1000(6)改成1000(1),1200(6)改成1200(1)"""
import os
import re
try:
    import main1
except:
    import renamer.main1 as main1


class RenameError(Exception):
    def __init__(self, text):
        Exception.__init__(self, text)
        pass


def rename2(path):
    dir = path
    path_list = main1.get_file_path(dir)

    list_ = []

    list800 = []
    list1000 = []
    list1200 = []

    for i in path_list:
        if '800' in i:
            list800.append(i)
        elif '1000' in i:
            list1000.append(i)
        elif '1200' in i:
            list1200.append(i)
    
    try:
        list800.sort(key=lambda x: int(re.search(r'\((\d+)\)', x).group(1)), reverse=False)     # type: ignore
        list1000.sort(key=lambda x: int(re.search(r'\((\d+)\)', x).group(1)), reverse=False)    # type: ignore
        list1200.sort(key=lambda x: int(re.search(r'\((\d+)\)', x).group(1)), reverse=False)    # type: ignore
    except:
        raise RenameError('文件名不符合规范')
    
    for index, i in enumerate(list800[0:5]):
        k = i
        match = re.search(r'\((\d+)\)', i)
        if match is not None:
            num = match.group(1)
        else:
            raise TypeError('没有匹配到括号内的数字')
        new_name = re.sub(r'\((\d+)\)', lambda match: f'({index+1})', i)

        try:
            if '800' in i:
                os.rename(k, new_name)
            elif '1000' in i:
                os.rename(k, new_name)
            elif '1200' in i:
                os.rename(k, new_name)
        except:
            list_.append((index, i))

    for index, i in enumerate(list1000[0:5]):
        k = i
        match = re.search(r'\((\d+)\)', i)
        if match is not None:
            num = match.group(1)
        else:
            raise TypeError('没有匹配到括号内的数字')
        new_name = re.sub(r'\((\d+)\)', lambda match: f'({index+1})', i)

        try:
            if '800' in i:
                os.rename(k, new_name)
            elif '1000' in i:
                os.rename(k, new_name)
            elif '1200' in i:
                os.rename(k, new_name)
        except:
            list_.append((index, i))

    for index, i in enumerate(list1200[0:5]):
        k = i
        match = re.search(r'\((\d+)\)', i)
        if match is not None:
            num = match.group(1)
        else:
            raise TypeError('没有匹配到括号内的数字')
        new_name = re.sub(r'\((\d+)\)', lambda match: f'({index+1})', i)

        try:
            if '800' in i:
                os.rename(k, new_name)
            elif '1000' in i:
                os.rename(k, new_name)
            elif '1200' in i:
                os.rename(k, new_name)
        except:
            list_.append((index, i))
    for index, i in list_:
        k = i
        match = re.search(r'\((\d+)\)', i)
        if match is not None:
            num = match.group(1)
        else:
            raise TypeError('没有匹配到括号内的数字')
        num_ = int(num)
        new_name = re.sub(r'\((\d+)\)', lambda match: f'({index+1})', i)

        if '800' in i:
            os.rename(k, new_name)
        elif '1000' in i:
            os.rename(k, new_name)
        elif '1200' in i:
            os.rename(k, new_name)

if __name__ == '__main__':
    rename2('D:\\41tm\\KC-41-XOU131\\main')