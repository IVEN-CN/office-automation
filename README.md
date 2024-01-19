# 实现自动化办公
    在日常办公，会经常遇到批量修改文件名或者按照颜色分类颜色文件的情况，花费很多时间，也会消耗精力，于是决定开发此程序
## init使用方法
首先要先进行颜色阈值的初始化——color_div/init.py

    # 结尾的main函数参数改成对应颜色的1200尺寸平铺图的完整路径
    main(r'D:\41short\KC-41-XOU128\1200(6).jpg')

    # 或者使用\\转义
    main('D:\\41short\\KC-41-XOU128\\1200(6).jpg')

### 运行init

    运行程序后会出现3个窗口，一个窗口调整阈值滑块，一个窗口显示原图片，一个窗口显示识别后的图片

    滑动阈值滑块，调整HSV颜色阈值，使在尽可能小的阈值范围将衣服尽可能多的显示白色

    调整area滑块，用尽可能大的值使得显示原图像的窗口出现完整的绿色框框住衣服

    调整chooes_area滑块，0对应模特的识别面积，1对应平铺图的识别面积

    滑动两个save滑块完成保存操作，然后esc退出程序

--! 注意，每个面积保存一次后，理论上来说不需要再调整 !--

## 主文件使用方法
首先提供所有颜色的1200尺寸的平铺图和普通无需裁剪的模特图，文件夹路径要求不能有中文（D:\41short\KC-41-XOU128\）
    
    调整office automation.py文件结尾main函数的参数如果事先就决定那个序号的图片不需要移动到主图文件夹，例如现在(7)号图片不需要移动到主图文件夹，那么参数修改为

    main('(7)',path=r'D:\41short\KC-41-XOU128')

    <!-- 需要注意的是，颜色分类并不一定准确，分类完成后必须检查！ -->

    事后再P尺寸1200的主图模特图，直接存在主图文件夹。然后打开cutter/cut.py在结尾函数调用的位置调整参数，比如有多个图片(A和B)都在主图路径(D:\41short\KC-41-XOU179\主图)下，并且A和B都是主图模特图，需要进行裁剪

    cut_cut('B.jpg','A.jpg',path=r'D:\41short\KC-41-XOU179\主图')

    运行文件

## 额外的功能
对于设计人员，有很多的图片在本地难以寻找，但是又有相似的图片，这个图片可能是原图片的缩放版本，现在想知道原图片的位置

    打开match/matcher.py，调整结尾的函数参数，第一个参数是原图片可能会存在的文件夹路径，第二个参数是需要寻找的图片的路径(现有图片)

    main('D:\\', 'C:\\user\\desktop\\1.png')
### 尚未开放完毕的功能
在许多设计公司，印花的图片可能存在共享网络的电脑上，现有需求，本地用户直接在共享网络文件中查找图片路径

    match/test.py文件是在测试在局域网共享网络中连接其他主机的共享文件夹，然后尝试在内读取图片文件

    现有难点：
        1.无法获取目标计算机文件下下的文件路径，只能获取文件夹的名次，若有在共享文件夹中有os.walk类似的方法似乎可以解决这个问题
        2.无法使用OpenCV的decode方法打开目标文件夹下的图片