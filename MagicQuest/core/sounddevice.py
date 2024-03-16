import os
import tempfile
import numpy as np
import sounddevice as sd
from scipy.io.wavfile import write
import keyboard

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
temp_dir = os.path.join(PROJECT_ROOT, 'DB')
os.makedirs(temp_dir, exist_ok=True)


def record_audio():
    print("准备录音，按下 't' 开始录音，再次按 't' 停止。")

    recording = []  # 初始化录音数组
    is_recording = False
    samplerate = 44100  # 采样率

    def callback(indata, frames, time, status):
        nonlocal recording
        if is_recording:
            # 将数据转换为numpy数组，并确保其具有正确的维度
            indata = np.array(indata, dtype=np.int16)
            # 如果是第一次接收数据，则直接赋值给recording
            if len(recording) == 0:
                recording = indata
            else:
                # 否则，将数据追加到recording数组的末尾
                recording = np.concatenate((recording, indata))

    with sd.InputStream(samplerate=samplerate, channels=2, dtype='int16', callback=callback):
        def on_press(event):
            nonlocal is_recording, recording
            if event.name == 't':
                if not is_recording:
                    print("开始录音...")
                    recording = []  # 重置录音数组
                    is_recording = True
                else:
                    print("停止录音...")
                    is_recording = False
                    save_recording(recording)
                    keyboard.unhook_all()  # 解除所有按键钩子

        keyboard.on_press(on_press)
        print("按 'esc' 键退出录音等待状态...")
        keyboard.wait('esc')


def save_recording(recording):
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.wav', dir=temp_dir, prefix='audio_', mode='wb+')
    write(temp_file.name, 44100, np.concatenate(recording))  # 保存录音
    print(f"录音结束，文件已保存为：{temp_file.name}")



# recording：一个列表，用于存储录音过程中的音频数据。
# is_recording：一个布尔值，标记是否正在录音。它被callback函数用于判断当前是否应该捕获音频数据。
# samplerate：定义音频的采样率。这里设置为44100Hz，这是一个常用的高质量音频采样率。
# stream：使用sounddevice.InputStream创建的音频输入流，它负责从麦克风捕获音频数据。
# 关键函数
# callback(indata, frames, time, status)：这是一个回调函数，由音频输入流（stream）在每次有新音频数据可用时调用。indata包含了最新捕获的音频数据。如果is_recording为True，则将indata追加到recording列表中。
#
# on_press(event)和on_release(event)：这两个函数分别处理键盘的按下和释放事件。当t键被按下时，on_press函数将is_recording设置为True，开始录音；当t键被释放时，on_release函数将is_recording设置为False，停止录音，并保存录音数据到一个临时文件中。
#
# 录音控制逻辑
# 通过keyboard.on_press(on_press)监听键盘按下事件，如果检测到t键被按下，就开始录音。
# 通过keyboard.on_release_key('t', on_release)监听t键的释放事件，当t键被释放，录音停止，录音数据被写入到临时文件中。
# keyboard.wait('esc')：这是程序的等待循环，让程序持续运行并监听键盘事件直到按下Esc键。这行代码确保了程序在完成录音前不会退出。你可以根据需要修改等待退出的键。
# 保存录音数据
# 当录音结束，即t键被释放时，在on_release函数内，使用tempfile.NamedTemporaryFile创建一个临时WAV文件，
# 并使用scipy.io.wavfile.write函数将录音数据写入此文件。这个临时文件位于DB目录下，文件名以audio_为前缀，保证了文件名的唯一性。
# 结束录音和清理资源
# 在录音数据被保存后，keyboard.unhook_all()被调用以取消所有键盘事件的监听，避免重复触发录音事件。同时，这也是清理资源的一部分，确保程序可以平稳地结束。
