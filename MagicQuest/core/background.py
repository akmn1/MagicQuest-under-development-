import ctypes


def set_desktop_background(image_path):
    """
    设置Windows桌面背景图片
    :param image_path: 图片的完整路径
    """
    # SPI_SETDESKWALLPAPER是设置桌面背景的操作码，20
    # 第二个参数为0表示更新用户配置文件，最后一个参数为0表示操作立即生效
    # 使用系统参数信息（SPI）函数设置桌面背景，并立即更改
    result = ctypes.windll.user32.SystemParametersInfoW(20, 0, image_path, 3)

    if not result:
        print("无法设置桌面背景。可能是由于图片路径错误或文件类型不支持。")
    else:
        print("桌面背景已成功更新。")


# 示例调用
image_path = r'E:\绘画文件\ziliao\图片\二次元参考\0b977391b98197322ece6627822f4b43f5a74f1b_raw.jpg'
set_desktop_background(image_path)
