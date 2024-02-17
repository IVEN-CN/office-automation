# 实现自动化办公
    在日常办公，会经常遇到批量修改文件名或者按照颜色分类颜色文件的情况，花费很多时间，也会消耗精力，于是决定开发此程序
## init使用方法
首先要先进行颜色阈值的初始化——color_div/init.py

首先使用终端terminal打开项目文件夹路径，激活python的venv虚拟环境

    .\venv\Scripts\activate
进入color_div文件夹

    cd color_div
运行init.py

    # 在命令结尾的-p(也可以是--path)是初始化图片的路径参数
    python init.py -p 'D:\PIC.jpg'

    # 或者
    python init.py --path 'D:\PIC.jpg'

### 运行init

    -运行程序后会出现3个窗口，一个窗口调整阈值滑块，一个窗口显示原图片，一个窗口显示识别后的图片

    -滑动阈值滑块，调整HSV颜色阈值，使在尽可能小的阈值范围将衣服尽可能多的显示白色

    -调整area滑块，用尽可能大的值使得显示原图像的窗口出现完整的绿色框框住衣服

    -调整chooes_area滑块，0对应模特的识别面积，1对应平铺图的识别面积

    -滑动两个save滑块完成保存操作，然后esc退出程序

--! 注意，每个面积保存一次后，理论上来说不需要再调整 !--

## 主文件使用方法
此项目需要一个工作文件夹，包含了已经初步完成的800x1200尺寸的平铺图，命名规则：1200(x)。x是编号，应该从6开始;对于模特图，应该是以数字命名：例如1,2,3等。但是其他数字似乎没有影响。

一个标准的工作文件夹应该如下图所示\
![example](.pic\example.jpg)

备份工作文件夹，以防出现意外

以上图的工作文件夹为例，程序会对所有图片进行裁剪和分类\
在终端执行命令(需要激活虚拟环境)
    
    #进入代码文件所在文件夹(例如)
    cd d:\office-automation

    #激活虚拟环境
    .\.venv\Scripts\activate

    # 运行程序，无需粘贴png图片(默认)，没有多颜色分类(多件童装的形式)(默认)，没有提供额外的主图文件夹(默认)，需要颜色分类，代码实例如下
    python officeautomation.py --path 'D:\42maleT-A2-2' --ifcolordiv True 

    # 运行程序，无需粘贴png图片(默认)，没有多颜色分类(多件童装的形式)(默认)，没有提供额外的主图文件夹(默认)，不需要需要颜色分类，代码实例如下
    python officeautomation.py --path 'D:\42maleT-A2-2' --ifcolordiv False

### 2.1版本新增功能：
添加了多颜色识别的功能，对于三颜色童装和双颜色通知提供了多颜色分类，在main函数的调用将morecolor参数改为True即可

### 2.2版本新增功能：
添加了png图片的粘贴，对于多件套装的童装需要粘贴png图片（两件装等），在main函数封装了stack参数，如果需要粘贴，将stack参数改为True,stack_path改为png的路径，position改为粘贴的位置坐标。

### 3.0版本新增：
修改为命令行传参形式

### 需要优化的部分：
对于不同衣服款式会有不同的颜色，在颜色识别的时候我们可以只识别那些会出现的颜色而不识别那些不会出现的颜色，例如款式U075只有颜色红，草绿，黄，雾霾蓝，那么在颜色识别的时候可以将识别彩兰，天蓝等颜色的代码区域注释掉(在代码前面加上#(井号)即可关闭相应的代码块)

    main(path=r'D:\41childA1', position=(140, 760), ifcolordiv=True, ifmain=True, morecolor=True, ifstack=True, stack_path=r'./2-02.png')

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