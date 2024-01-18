import cv2
import os
from skimage.metrics import structural_similarity


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

    if img1.shape != img2.shape:
        height, width = img1.shape[:2]
        img2 = cv2.resize(img2, (width, height), interpolation=cv2.INTER_CUBIC)

    # 将图像转换为灰度
    gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

    # 计算SSIM,score越大相似度越高，diff越小
    (score, diff) = structural_similarity(gray1, gray2, full=True)
    print(f"图像SSIM:{score}")
    return score


def main(dir, img2_path):     # 绝对路径
    """比较文件夹下所有图片与模板图片的相似度
    dir: 文件夹路径
    img2_path: 图片模板的路径"""
    list_img = []
    file_path = get_file_path(dir)
    for i in file_path:
        similarity = compare_img(i, img2_path)
        if similarity > 0.7:
            print(f'路径为{i}的图片与模板图片的相似度为{similarity}')
            list_img.append(i)
    return list_img, similarity


if __name__ == "__main__":
    main('D:\\code_python\\pic_reserch\\match', 'D:\\code_python\\pic_reserch\\match\\1.png')