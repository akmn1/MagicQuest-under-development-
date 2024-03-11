import ctypes
import os

# 定义光标类型与SPI_* 常量的映射
CURSOR_TYPES = {
    "Arrow": 32512,  # 标准箭头
    "IBeam": 32513,  # 文本选择
    "Wait": 32514,  # 等待
    "Crosshair": 32515,  # 十字
    "UpArrow": 32516,  # 向上箭头
    "SizeNWSE": 32642,  # 斜杠调整大小
    "SizeNESW": 32643,  # 反斜杠调整大小
    "SizeWE": 32644,  # 水平调整大小
    "SizeNS": 32645,  # 垂直调整大小
    "SizeAll": 32646,  # 四方向调整大小
    "No": 32648,  # 禁止/不可用
    "Hand": 32649,  # 手形（链接选择）
    "AppStarting": 32650,  # 应用启动
    "Help": 32651,  # 帮助
}


def change_cursor(cursor_name, cursor_path):
    """
    更改特定操作上下文的鼠标样式。

    :param cursor_name: 操作上下文的光标名称（如"Arrow", "IBeam"）。
    :param cursor_path: 新光标文件的路径。
    """
    cursor_type = CURSOR_TYPES.get(cursor_name)
    if not cursor_type:
        print(f"未知的光标类型: {cursor_name}")
        return

    # 设置光标
    result = ctypes.windll.user32.SetSystemCursor(ctypes.windll.user32.LoadCursorFromFileW(cursor_path), cursor_type)

    if not result:
        print(f"无法更改 {cursor_name} 光标样式。请检查光标文件路径和格式。")
    else:
        print(f"{cursor_name} 光标样式已成功更新。")
