"""将750X1000文件夹下的所有文件改为1000开头，后面接括号，括号的数字从6开始，例如1000(6)
   将1200X800文件夹下的所有文件改成1200开头，后面接括号，括号的数字从6开始，例如1200(6)
   将800X800文件夹下的所有文件改成800开头，后面接括号，括号的数字从6开始，例如800(6)"""
import os

def get_file_path(file_dir) -> list:
    """获取相对路径下文件夹的所有文件的路径
    file_dir: 文件夹路径"""
    file_path = []
    for root, dirs, files in os.walk(file_dir):
        for file in files:
            file_path.append(os.path.join(root, file))
    return file_path

def _rename_file(file_path:str, new_name:str):
    """重命名文件
    file_dir: 文件路径
    new_name: 新文件名"""
    os.rename(file_path, os.path.join(os.path.dirname(file_path), new_name))

def rename_file(file_path:str, num:int=1):
    """如果文件在700X1000文件夹下，那么该文件夹下的所有文件都改为1000开头，后面接括号，括号的数字从6开始，例如1000(6)
    如果文件在1200X800文件夹下，那么该文件夹下的所有文件都改成1200开头，后面接括号，括号的数字从6开始，例如1200(6)"""
    num = str(num)
    if "700X1000" in file_path:
        _rename_file(file_path,
                    f"1000({num}).jpg")
    elif "800X1200" in file_path:
        _rename_file(file_path,
                    f"1200({num}).jpg")
    elif "800X800" in file_path:
        _rename_file(file_path,
                    f"800({num}).jpg")
        
def len_dir(file_dir:str):
    """获取文件夹下文件的数量
    file_dir: 文件夹路径"""
    return len(get_file_path(file_dir))

def divide_dir(root:list):
    global lst800, lst1200, lst1000
    lst800 = []
    lst1200 = []
    lst1000 = []
    for i in root:
        if "800X800" in i:
            lst800.append(i)
        elif "800X1200" in i:
            lst1200.append(i)
        elif "700X1000" in i:
            lst1000.append(i)

def main(path:str):
    file_dir = get_file_path(path)
    divide_dir(file_dir)
    for i in range(len(lst800)):
        rename_file(lst800[i], i+6)
    for i in range(len(lst1200)):
        rename_file(lst1200[i], i+6)
    for i in range(len(lst1000)):
        rename_file(lst1000[i], i+6)
        
if __name__ == "__main__":
    main('./U007')
