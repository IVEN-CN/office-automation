from smb.SMBConnection import SMBConnection
import io
import cv2
import numpy as np

# 创建一个SMB连接
conn = SMBConnection('Administrator', '', 'PC-IVEN', 'hzrc-01', use_ntlm_v2 = True)

# 连接到服务器
assert conn.connect('192.168.5.18', 139)

# # 列出共享文件夹下的所有文件
# file_paths = []
# for file_info in conn.listPath('瑞诚服装设计组可更改', '/'):
#     file_paths.append(file_info.filename)
# print(file_paths)

# 打开一个文件并读取其内容
file_obj = io.BytesIO()
file_attributes, filesize = conn.retrieveFile('瑞诚服装设计组可更改', 'L048-DMKB-TZ.jpg', file_obj)

# 将文件对象转换为NumPy数组
file_bytes = np.asarray(bytearray(file_obj.read()), dtype=np.uint8)

# 使用OpenCV读取图片
image = cv2.imdecode(file_bytes, cv2.IMREAD_UNCHANGED)

# 显示图片
cv2.imshow('image', image)
cv2.waitKey(0)
cv2.destroyAllWindows()