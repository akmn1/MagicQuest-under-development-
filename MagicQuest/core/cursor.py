import os
import ctypes
import winreg as reg

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
cursor_dir = os.path.join(PROJECT_ROOT, 'DB', 'cursor_resources')

cursor_files = {
    "Arrow": "normal.cur",
    "Help": "help.cur",
    "AppStarting": "working.ani",
    "Wait": "busy.ani",
    "Crosshair": "precision.cur",
    "IBeam": "text.cur",
    "Hand": "link.cur",
    "No": "unavailable.cur",
    "SizeNS": "vertical.cur",
    "SizeWE": "horizontal.cur",
    "SizeNWSE": "diagonal1.cur",
    "SizeNESW": "diagonal2.cur",
    "SizeAll": "move.cur",
    "UpArrow": "alternate.cur",
    # 添加其他光标样式...
}

def apply_cursor():
    try:
        with reg.OpenKey(reg.HKEY_CURRENT_USER, r"Control Panel\Cursors", 0, reg.KEY_SET_VALUE) as key:
            for cursor_name, file_name in cursor_files.items():
                file_path = os.path.join(cursor_dir, file_name)
                if os.path.isfile(file_path):
                    reg.SetValueEx(key, cursor_name, 0, reg.REG_SZ, file_path)
                else:
                    print(f"文件不存在，跳过：{file_path}")
            reg.SetValueEx(key, "Scheme Source", 0, reg.REG_SZ, "User Defined")
        # 使用ctypes安全调用SystemParametersInfoW
        ctypes.windll.user32.SystemParametersInfoW(0x0057, 0, None, 0x02 | 0x01)
        print("光标样式已成功更新。")
    except Exception as e:
        print(f"更新光标样式时出错：{e}")



def re_cursor():
    # 打开光标设置的注册表项
    with reg.OpenKey(reg.HKEY_CURRENT_USER, r"Control Panel\Cursors", 0, reg.KEY_SET_VALUE) as key:
        # 遍历所有光标设置，将它们重置为默认值（空字符串）
        reg.SetValueEx(key, "AppStarting", 0, reg.REG_SZ, "")
        reg.SetValueEx(key, "Arrow", 0, reg.REG_SZ, "")
        reg.SetValueEx(key, "Crosshair", 0, reg.REG_SZ, "")
        reg.SetValueEx(key, "Hand", 0, reg.REG_SZ, "")
        reg.SetValueEx(key, "Help", 0, reg.REG_SZ, "")
        reg.SetValueEx(key, "IBeam", 0, reg.REG_SZ, "")
        reg.SetValueEx(key, "No", 0, reg.REG_SZ, "")
        reg.SetValueEx(key, "NWPen", 0, reg.REG_SZ, "")
        reg.SetValueEx(key, "SizeAll", 0, reg.REG_SZ, "")
        reg.SetValueEx(key, "SizeNESW", 0, reg.REG_SZ, "")
        reg.SetValueEx(key, "SizeNS", 0, reg.REG_SZ, "")
        reg.SetValueEx(key, "SizeNWSE", 0, reg.REG_SZ, "")
        reg.SetValueEx(key, "SizeWE", 0, reg.REG_SZ, "")
        reg.SetValueEx(key, "UpArrow", 0, reg.REG_SZ, "")
        reg.SetValueEx(key, "Wait", 0, reg.REG_SZ, "")
        # 移除可能设置的“方案”名称
        reg.DeleteValue(key, "Scheme Source")
    # 通知系统光标已更改
    ctypes.windll.user32.SystemParametersInfoW(0x0057, 0, None, 0)


