import cv2
import os

def get_file_path(file_dir) -> list:
    """获取相对路径下文件夹的所有文件的路径
    file_dir: 文件夹路径"""
    file_path = []
    for root, dirs, files in os.walk(file_dir):
        for file in files:
            file_path.append(os.path.join(root, file))
    return file_path

def compare_img(img1_path:str, img2_path:str) -> float:
    """比较两张图片的相似度
    img1_path: 图片1的路径
    img2_path: 图片模板的路径"""
    lt0 = [".jpg", ".png", ".jpeg"]
    if img1_path[-4:] not in lt0 or img2_path[-4:] not in lt0:
        return 0
    img1 = cv2.imread(img1_path)
    img2 = cv2.imread(img2_path)
    # 计算图片的直方图
    hist1 = cv2.calcHist([img1], [0], None, [256], [0, 256])
    hist2 = cv2.calcHist([img2], [0], None, [256], [0, 256])
    # 计算直方图的相似度
    similarity = cv2.compareHist(hist1, hist2, cv2.HISTCMP_CORREL)
    return similarity

def main(dir, img2_path):     # 绝对路径
    """比较文件夹下所有图片与模板图片的相似度
    dir: 文件夹路径
    img2_path: 图片模板的路径"""
    list_img = []
    file_path = get_file_path(dir)
    for i in file_path:
        similarity = compare_img(i, img2_path)
        if similarity > 0.9:
            print(f'路径为{i}的图片与模板图片的相似度为{similarity}')
            list_img.append(i)
    return list_img, similarity

if __name__ == "__main__":
    main('D:\\code_python\\pic_reserch\\match', 'D:\\code_python\\pic_reserch\\match\\1.png')